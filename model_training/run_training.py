import subprocess
import os

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(stderr)
    else:
        print(stdout)

# tokenizers = ["REMI", "MIDILike", "TSD", "Structured", "CPWord", "MuMIDI", "Octuple"]
tokenizers = ["REMI"]



# Komenda przygotowania danych:
# for tokenizer in tokenizers:
#     # Ścieżka do pliku tekstowego
#     input_file_path = os.path.join("prepare_data\\data\\prepped_data", f"{tokenizer}.txt")
#     output_file_path = os.path.join("generated_data\\txt", f"{tokenizer}.txt")
    
print("Preparing data for training...")
prepare_command = (
    f"python data/shakespeare_char/prepare.py"
)

run_command(prepare_command)

print("Trainging...")
# Komenda treningu
train_command = (
    f"python train.py config/train_shakespeare_char.py --device=cpu --compile=False --eval_iters=20 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=2000 --lr_decay_iters=2000 --dropout=0.0"
)

run_command(train_command)

print("Saving generated data...")
# Komenda generowania próbek
sample_command = f"python sample.py --out_dir=out-tokenizer --device=cpu"
run_command(sample_command)
