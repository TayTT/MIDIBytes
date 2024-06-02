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

# URL do pobrania
url = "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip"
# Ścieżka do rozpakowania pliku
extract_to = ".\\prepare_data\\data\\midi\\"

# Uruchomienie funkcji
download_and_extract_zip(url, extract_to)