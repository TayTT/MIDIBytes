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
python sample.py --out_dir=[insert output folder] 
```

The script will generate output.json file with generated tokens and save it in *generated_data\txt\output.json* path. If you want to listen to generated music copy *output.json* to prepare_data folder and run test.py. This script will generate test.midi file you can listen to.

# Evalutation:

Add a folder with tokenizer as name. Insert .pt and meta.pkl files inside.

Configuration for evaluation can be changed in a *models\generation_config.py* file. You can change tokenizer, prompts for models, number of samples and different parameters.

To run evaluation enter following command:

```sh
python models\run_evaluation.py
```

Generated midi files and computed errors will be in *data\generated_data* folder.

To check if generated tokens are correct, TSE (Token syntax error) metrics were used [1].


[1]"Impact of time and note duration tokenizations on deep learning symbolic music modeling" by Nathan Fradet . 