from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer, GPT2LMHeadModel, AutoConfig, DataCollatorForLanguageModeling, Trainer, TrainingArguments
import time

context_length = 128
dataset = load_dataset("TayTT/REMI_set")
tokenizer = AutoTokenizer.from_pretrained("gpt2") #BPE

def int_to_char(example):
    example['tokens'] = [str(token) for token in example['tokens']]
    return example


# def tokenize(piece):
#     outputs = tokenizer(
#         piece["tokens"],
#         # turncation=False,
#         max_length=CONTEXT_LENGTH,
#         return_overflowing_tokens=False)

#     return outputs

# tokenized_datasets = dataset.map(
#     tokenize, batched=True, remove_columns=dataset['train'].column_names)

dataset = dataset.map(int_to_char, batched=True)

outputs = tokenizer(
    dataset["train"][:2]["tokens"],
    truncation=True,
    max_length=context_length,
    return_overflowing_tokens=True,
    return_length=True,
)

def tokenize(element):
    outputs = tokenizer(
        element["tokens"],
        truncation=True,
        max_length=context_length,
        return_overflowing_tokens=True,
        return_length=True,
    )
    input_batch = []
    for length, input_ids in zip(outputs["length"], outputs["input_ids"]):
        if length == context_length:
            input_batch.append(input_ids)
    return {"input_ids": input_batch}


tokenized_datasets = dataset.map(
    tokenize, batched=True, remove_columns=dataset["train"].column_names
)

def evaluate():
    model.eval()
    losses = []
    for step, batch in enumerate(eval_dataloader):
        with torch.no_grad():
            outputs = model(batch["input_ids"], labels=batch["input_ids"])

        losses.append(accelerator.gather(outputs.loss))
    loss = torch.mean(torch.cat(losses))
    try:
        perplexity = torch.exp(loss)
    except OverflowError:
        perplexity = float("inf")
    return loss.item(), perplexity.item()




config = AutoConfig.from_pretrained(
    "gpt2",
    vocab_size=len(tokenizer),
    n_ctx=context_length,
    bos_token_id=tokenizer.bos_token_id,
    eos_token_id=tokenizer.eos_token_id,
)

model = GPT2LMHeadModel(config)
model_size = sum(t.numel() for t in model.parameters())
print(f"GPT-2 size: {model_size/1000**2:.1f}M parameters")

tokenizer.pad_token = tokenizer.eos_token
data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

out = data_collator([tokenized_datasets["train"][i] for i in range(5)])
for key in out:
    print(f"{key} shape: {out[key].shape}")

args = TrainingArguments(
    output_dir="codeparrot-ds",
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    evaluation_strategy="steps",
    eval_steps=5_000,
    logging_steps=5_000,
    gradient_accumulation_steps=8,
    num_train_epochs=1,
    weight_decay=0.1,
    warmup_steps=1_000,
    lr_scheduler_type="cosine",
    learning_rate=5e-4,
    save_steps=5_000,
    fp16=False,
    push_to_hub=True,
    save_strategy="steps",
    restore_callback_states_from_checkpoint=True
)

trainer = Trainer(
    model=model,
    tokenizer=tokenizer,
    args=args,
    data_collator=data_collator,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["valid"],
)

print("Training!")
start = time.time()

trainer.train('C:/Users/Tay/VSCode/MIDIBytes/codeparrot-ds/runs/May29_00-38-42_DESKTOP-UVR5C2O\events.out.tfevents.1716935922.DESKTOP-UVR5C2O.6744.0')
trainer.save_model('C:/Users/Tay/VSCode/MIDIBytes/src/model')
trainer.save_state('C:/Users/Tay/VSCode/MIDIBytes/src/model')
end = time.time()

print("Time elapsed: ", end-start)
