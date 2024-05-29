# Config file

In config.py you can find all the project paths used in fetch_maestro.py. 

# Data preparation

If you want to generate new tokens, you need to run fetch_maestro.py. It will download the data set and save it in prepare_data\data\midi.

In prepare_data folder you can find a script for generating .txt files containing tokens for training. If you want to change the configurations for tokenizers you can change "tokenizer.set_config()" line adding different configuration settings.

The .txt files ready for training are saved in prepare_data\data\prepped_data path and were generated for default configuration.

# Training

If you want to train models for different tokenizers you can run a file **run_training.py** in model_training folder. It's supposed to train models for different tokenizers on the data prepped in previous step. You can change the parameters of trainging in **train_command**.

After training run a following command:

``` sh
python sample.py --out_dir=out-shakespeare-char --device=cpu
```

The script will generate output.json file with generated tokens and save it in *generated_data\txt\output.json* path. If you want to listen to generated music copy *output.json* to prepare_data folder and run test.py. This script will generate test.midi file you can listen to.

# To fix:

1. Fixing generated tokens - data needs to be checked before converting to midi (it has to be in a accepted range). 
2. Is there a way of controling the generated file length? Generated midis are short