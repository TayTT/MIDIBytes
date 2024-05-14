import json

class TokensPrep:
    def __init__(self, file_path):
        self.file_path = file_path




reader = TokensPrep('./../../data/tokens/REMI/0.json')
json_data = reader.read_ids()
if json_data:
    print(json_data)
    print(type(json_data))