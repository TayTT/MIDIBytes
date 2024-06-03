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
- music21  
- matplotlib  

## Architektura systemu

Aplikacja znajduje się na branchu **main** natomiast przygotowanie danych oraz trenowanie na branchu **nano-prep**.

### Opis modułów
#### Moduł aplikacji
##### Ogólny opis modułu aplikacji

Moduł aplikacji umożliwia użytkownikom wybór tokenizatorów, wgrywanie plików MIDI, określenie długości sekwencji startowej do generacji oraz generowanie i ocenę wynikó przy pomocy prostego i intuicyjnego interfejsu. Proces składa się z kilku kroków:

1. **Wybór tokenizatorów**
   - Użytkownik wybiera z listy tokenizatory, które mają być użyte. Można wybrać co najmniej jeden, maksymalnie wszystkie.
   - Po dokonaniu wyboru użytkownik klika "Continue".

2. **Wgrywanie plików MIDI**
   - Użytkownik wgrywa jeden plik MIDI.
   - Aplikacja akceptuje tylko pliki typu MIDI.

3. **Określenie procentowej wartości użycia pliku**
   - Użytkownik określa, ile procentowo z wgrywanego pliku zostanie wykorzystane jako początek sekwencji MIDI do modelu generatywnego.
   - Pasek procentowy umożliwia łatwe ustawienie tej wartości.

4. **Generowanie i ewaluacja wyników**
   - Okienko rozwijalne wyświetla logi z działania aplikacji, pozwalając użytkownikowi śledzić postęp.
   - Po zakończeniu generowania wyników użytkownik może odtworzyć pliki, pobrać je oraz zobaczyć tabelę z metrykami.
   - Jeśli użytkownik chce wygenerować nową próbkę, klika przycisk "start again".

##### Moduł treningu i przygotowania modeli

Moduł ten obejmuje następujące kroki:

1. **Pobieranie datasetu:** Skrypt fetch_maestro.py pobiera dataset Maestro w formacie MIDI i tworzy strukturę folderów do przechowywania danych.

2. **Przygotowanie danych:** Skrypt prep_data.py konwertuje dane MIDI do plików tekstowych (.txt) za pomocą tokenizatorów, zapisując je w odpowiednim katalogu.

3. **Trenowanie modelu:** Skrypty w folderze model_training przygotowują dane, konfigurują parametry i uruchamiają trenowanie modelu, z możliwością logowania postępów.

4. **Ewaluacja modelu:** Skrypt run_evaluation.py ocenia model poprzez obliczenie błędów, analizę dźwięków i ocenę subiektywną wygenerowanej muzyki, zapisując wyniki w katalogu data\generated_data.

Moduł zapewnia pełny cykl pracy od pobierania danych po trenowanie i ewaluację modeli generujących muzykę.


## Instalacja i konfiguracja

Aby skonfigurować aplikację, konieczne jest zainstalowanie i skonfigurowanie kilku narzędzi i bibliotek. Poniżej znajduje się opis kroków, które należy wykonać:

#### 1. Python 3.12
Zainstaluj Python 3.12, który jest wymagany do uruchomienia aplikacji. Możesz pobrać go z [oficjalnej strony Pythona](https://www.python.org/downloads/).

#### 2. Biblioteki Python
By móc korzystać z modułu trenowania modeli należy pobrać odpowiednie biblioteki. Możesz to zrobić za pomocą polecenia `pip` i pliku `requirements.txt`. Stwórz plik `requirements.txt` i umieść w nim następujące biblioteki:

```
miditok==3.0.3
streamlit
midi2audio==0.1.1
pathlib==1.0.1
symusic==0.4.3
torch==2.2.1
pydub==0.25.1
fluidsynth==0.2
pytorch
numpy
transformers
prettymidi
wandb
music21
matplotlib
```

Następnie uruchom komendę:

```sh
pip install -r requirements.txt
```

#### 3. Visual Studio Code (VSCode)
Visual Studio Code (VSCode) jest zalecanym edytorem kodu do pracy nad projektem. Możesz pobrać go z [oficjalnej strony Visual Studio Code](https://code.visualstudio.com/).

Po zainstalowaniu VSCode, warto zainstalować następujące rozszerzenia:
- Python
- Docker
- GitLens

#### 4. Git
By pobrać kod źródłowy sklonuj repozytorium projektu przy użyciu komendy:

```sh
git clone https://github.com/TayTT/MIDIBytes.git
```

#### 5. Docker
Docker umożliwia tworzenie i uruchamianie aplikacji w kontenerach. Możesz pobrać go z [oficjalnej strony Docker](https://www.docker.com/products/docker-desktop).

Po zainstalowaniu programu Docker, uruchom go i upewnij się, że działa poprawnie.

#### 6. Konfiguracja aplikacji
By skonfigurować aplikację należy przejść do folderu src, a następnie uruchomić komendy:

```sh
docker compose build
```
```sh
docker compose up
```

## Użycie
### Korzystanie z aplikacji
Aplikacja pozwala na ocenę jakości generacji muzyki dla 6 tokenizatorów. Aby jej użyć aplikacji należy skorzystać z konteneryzatora Docker.

**Uruchamianie aplikajci przy użyciu Docker'a**
1. Uruchomić środowisko Docker, np. aplikację desktopową Docker.
2. W folderze src uruchomić komendę docker compose build:
	```sh
	 cd src
  	```
	```sh
	 docker compose build
  	```
4. Po zbudowaniu kontenera:
	```sh
	  docker compose up
	 ```
5. Aplikacja dostępna jest w przeglądarce internetowej pod adresem:
	```sh
	 localhost:8501
	 ```

### Korzystanie z modułu do trenowania modeli

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
Ocena modelu polega na obliczeniu błędów TSE (token syntax error) [1], zakresu wysokości dźwieku, zakresu dynamiki utworu, współczynników harmonii oraz na ocenie subiektywnej po odsłuchu wygenerowanego nagrania. By uruchomić skrypt należy uruchomić poniższą komendę:

```sh
python models\run_evaluation.py
```

By zmienić parametry oceny należy edytować stałe znajdujące się w pliku *models\generation_config.py*. Możliwa jest edycja ilości wygenerowanych sampli, zmiany pliku rozpoczynającego generowaną sekwencję, zmianę długości sekwencji startowej oraz kilku dodatkowych parametrów.

Wyniki generacji wyświetlane są na ekran oraz zapisane do pliku w ścieżce *data\generated_data*.


[1] "Impact of time and note duration tokenizations on deep learning symbolic music modeling" by Nathan Fradet.
