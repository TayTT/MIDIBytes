import os
import pickle
import torch

from model import GPTConfig, GPT
from contextlib import nullcontext
from config import MODEL_DIR, GENERATED_SAMPLE_DIR
from utils import replace_double_commas, remove_single_comma, remove_unmatched_brackets, check_values, purge_dir

'''
This file contains sampling script to generate new tokens
'''

# -----------------------------------------------------------------------------
num_samples = 1 # number of samples to draw
temperature = 0.8 # 1.0 = no change, < 1.0 = less random, > 1.0 = more random, in predictions | 0.8
top_k = 300 # retain only the top_k most likely tokens, clamp others to have 0 probability | 200
seed = 1337
device = 'cpu' # examples: 'cpu', 'cuda', 'cuda:0', 'cuda:1', etc.
dtype = 'bfloat16' if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else 'float16' # 'float32' or 'bfloat16' or 'float16'
exec(open('configurator.py').read()) # overrides from command line or config file


model_dir = MODEL_DIR
generated_sample_dir = GENERATED_SAMPLE_DIR
# -----------------------------------------------------------------------------
    
def create_sample(name, start, mx_new_t):
    # check whether name suggests using BPE
    if "BPE" in name:
        bpe_encoded = "true"
    else:
        bpe_encoded = "false"
        
    tokenizer_name = name.replace("_BPE", "")
        
    # check whether model dir exists, if not then terminate
    if not os.path.exists(model_dir): raise ValueError("Model not found")
        
    # create output dir
    purge_dir(generated_sample_dir)
    
    #set custom output length
    max_new_tokens = mx_new_t

    # load params
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cuda.matmul.allow_tf32 = True # allow tf32 on matmul
    torch.backends.cudnn.allow_tf32 = True # allow tf32 on cudnn
    device_type = 'cuda' if 'cuda' in device else 'cpu' # for later use in torch.autocast
    ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
    ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)

    # model
    # init from a model saved in a specific directory
    ckpt_path = os.path.join(model_dir, f'{name}.pt')
    checkpoint = torch.load(ckpt_path, map_location=device)
    gptconf = GPTConfig(**checkpoint['model_args'])
    model = GPT(gptconf)
    state_dict = checkpoint['model']
    unwanted_prefix = '_orig_mod.'
    for k,v in list(state_dict.items()):
        if k.startswith(unwanted_prefix):
            state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
    model.load_state_dict(state_dict)

    model.eval()
    model.to(device)

    # load meta
    meta_path = os.path.join(model_dir, f'{name}.pkl')
    print(f"Loading meta from {meta_path}...")
    with open(meta_path, 'rb') as f:
        meta = pickle.load(f)
    stoi, itos = meta['stoi'], meta['itos']
    encode = lambda s: [stoi[c] for c in s]
    decode = lambda l: ''.join([itos[i] for i in l])

    start_ids = encode(start)
    x = (torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...])

    # run generation
    output = '{"ids": [['
    with torch.no_grad():
        with ctx:
            y = model.generate(x, max_new_tokens, temperature=temperature, top_k=top_k)
            decoded = decode(y[0].tolist())
            output += decoded
                
    # save output
    output = replace_double_commas(output)
    output = check_values(output)
    if tokenizer_name == "CPWord"  or tokenizer_name == "MuMIDI" or tokenizer_name == "Octuple":
        output = remove_unmatched_brackets(output)
    output = remove_single_comma(output)
    
    out_sample_location = os.path.join(generated_sample_dir, f'{name}.json')
    with open(os.path.join(out_sample_location), "w") as file:
        file.write(output)
        file.write(f"]], \"ids_bpe_encoded\": [{bpe_encoded}]")
        file.write("}")
        
    return os.path.join(out_sample_location)