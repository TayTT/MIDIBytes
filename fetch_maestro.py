import requests
import zipfile
import os

def download_and_extract_zip(url, extract_to):
    # Pobieranie pliku
    response = requests.get(url)
    zip_path = os.path.join(extract_to, "temp.zip")

    # Zapisywanie pobranego pliku
    with open(zip_path, 'wb') as file:
        file.write(response.content)
    
    # Rozpakowywanie pliku ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    
    # Usunięcie tymczasowego pliku ZIP
    os.remove(zip_path)
    
def create_folders():
    # Ścieżka do głównego folderu
    base_dir = "prepare_data"
    
    # Ścieżka do folderu 'data'
    data_dir = os.path.join(base_dir, "data")
    
    # Lista nazw podfolderów
    folders = ["midi", "prepped_data", "tokens"]
    
    # Tworzenie folderu 'data', jeśli nie istnieje
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Utworzono folder: {data_dir}")
    else:
        print(f"Folder {data_dir} już istnieje")
    
    # Tworzenie podfolderów wewnątrz folderu 'data'
    for folder in folders:
        # Ścieżka do aktualnego podfolderu
        folder_path = os.path.join(data_dir, folder)
        
        # Tworzenie podfolderu, jeśli nie istnieje
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Utworzono folder: {folder_path}")
        else:
            print(f"Folder {folder_path} już istnieje")
    
    # Lista nazw podfolderów wewnątrz folderu 'tokens'
    tokens_folders = ["REMI", "MIDILike", "TSD", "Structured", "CPWord", "MuMIDI", "Octuple"]
    
    # Ścieżka do folderu 'tokens'
    tokens_dir = os.path.join(data_dir, "tokens")
    
    # Tworzenie podfolderów wewnątrz folderu 'tokens'
    for folder in tokens_folders:
        # Ścieżka do aktualnego podfolderu
        folder_path = os.path.join(tokens_dir, folder)
        
        # Tworzenie podfolderu, jeśli nie istnieje
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Utworzono folder: {folder_path}")
        else:
            print(f"Folder {folder_path} już istnieje")

create_folders()

# URL do pobrania
url = "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip"
# Ścieżka do rozpakowania pliku
extract_to = ".\\prepare_data\\data\\midi\\"

# Uruchomienie funkcji
download_and_extract_zip(url, extract_to)