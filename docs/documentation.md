# Badanie wpływu różnych metod tokenizacji na jakość muzyki generowanej za pomocą modeli symbolicznych

## Dokumentacja techniczna

### Wyszukiwanie informacji muzycznych

**Autorzy:**  
Kamil Jabłoński, Marlena Podleśna, Barbara Bańczyk

---

## Spis treści
1. [Wprowadzenie](#wprowadzenie)
   - [Cel projektu](#cel-projektu)
   - [Zakres](#zakres)
   - [Wymagania](#wymagania)
2. [Architektura systemu](#architektura-systemu)
   - [Opis modułów](#opis-modułów)
3. [Instalacja i konfiguracja](#instalacja-i-konfiguracja)
4. [Użycie](#użycie)
5. [Struktura katalogów i plików](#struktura-katalogów-i-plików)
6. [Testowanie](#testowanie)

---

## Wprowadzenie

### Cel projektu
Celem projektu było zbadanie wpływu metod tokenizacji na jakość generowanej muzyki w formatach symbolicznych.

### Zakres
Projekt obejmuje implementację różnych metod tokenizacji, porównanie wpływu samej tokenizacji na pliki midi, trening modeli symbolicznych na zbiorze danych muzycznych w formacie midi oraz ewaluację jakości generowanej muzyki.

### Wymagania
Poniżej przedstawione są wymagania systemowe:
- Python 3.12
- miditok 3.0.3
- streamlit
- midi2audio 0.1.1
- pathlib 1.0.1
- symusic 0.4.3
- torch 2.2.1
- pydub 0.25.1
- fluidsynth 0.2
- Docker
- pytorch
- numpy
- transformers
- prettymidi
- wandb

## Architektura systemu

Aplikacja znajduje się na branchu **main** natomiast przygotowanie danych oraz trenowanie na branchu **nano-prep**.

### Opis modułów
#### Moduł z brancha nano-prep
1. **Pobieranie datasetu i tworzenie struktury folderów**

Poniższa komenda umożliwia pobranie datasetu Maestro i stwarza strukturę folderów.

```sh
python .\fetch_maestro.py 
```

2. **Przygotowanie danych do trenowania**

Poniższa komenda tworzy pliki .txt dla wybranych tokenizatorów i zapisuje je w *prepare_data\data\prepped_data* nadając nazwe pliku typu **nazwa_tokenizatora**.txt.

```sh
python .\prepare_data\prep_data.py
```

3. **Trenowanie modelu**

W celu wytrenowania modelu trzeba najpierw uruchomić poniższe komendy. 

Przejdź do folderu trenowania
```sh
cd model_training
```

Uruchom komendę prepare. Służy ona do stworzenia plików meta.pkl potrzebnych później przy tworzeniu sampli modelu. Jako argument wywołania podaje się nazwę pliku txt, jeśli nie zostanie podana nazwa program nie wykona się.
```sh
python data/tokenizer/prepare.py --file_name=REMI.txt
```

By uruchomić pętlę należy uruchomić poniższą komendę. W celu włączenia funkcji logowania postępów należy w pliku konfiguracyjnym *config/train_tokenizer.py* zmienić parametr **wandb_log** na True. 
```sh
python train.py config/train_tokenizer.py
```
W pliku *model_training\config\train_tokenizer.py* znajduje się konfiguracja parametrów uczenia, którą można zmienić w ramach trenowania

4. **Ewaluacja modelu**
Ocena modelu polega na obliczeniu błędów TSE (token syntax error) [1] oraz ocenie subiektywnej po odsłuchu wygenerowanego nagrania. By uruchomić skrypt należy uruchomić poniższą komendę:

```sh
python models\run_evaluation.py
```

By zmienić parametry oceny należy edytować stałe znajdujące się w pliku *models\generation_config.py*. Możliwa jest edycja ilości wygenerowanych sampli, zmiany pliku rozpoczynającego generowaną sekwencję, zmianę długości sekwencji startowej oraz kilku dodatkowych parametrów.

Wyniki generacji wyświetlane są na ekran oraz zapisane do pliku w ścieżce *data\generated_data*.

#### Moduł z brancha main


## Instalacja i konfiguracja

## Użycie

## Struktura katalogów i plików

## Testowanie

[1] "Impact of time and note duration tokenizations on deep learning symbolic music modeling" by Nathan Fradet.