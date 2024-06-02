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


print("Generating prompt...")
prompt_command = (
    f"python .\\models\\generate_prompt.py"
)

run_command(prompt_command)

print("Generating samples...")
sample_command = (
    f"python .\\models\\sample.py"
)

run_command(sample_command)

print("Evaluation, generating midi file...")

eval_command = f"python .\\models\\evaluation.py"
run_command(eval_command)
