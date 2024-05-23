# **Opis badań**
**Wpływ tokenizacji na pliki MIDI**:
Pobrano 17 plików MIDI dla których obliczono trzy parametry:
* end time - za pomocą biblioteki prettyMIDI
* estimated tempo - za pomocą biblioteki prettyMIDI
* file size - funkcja os getsize
Następnie dokonano tokenizacji tych plików za pomocą tokenizatorów: "REMI", "MIDILike", "TSD", "Structured", "CPWord", "MuMIDI", "MMM", "Octuple".
Otrzymane dane przedstawiono na wykresach gdzie na osi x oznaczane były wartości parametrów dla pliku oryginalnego, a na osi y wartości dla pliku po tokenizacji danym tokenizatorem. Oczekiwanym efektem byłoby uzyskanie funkcji f(x) = x - oznacza to, że dany parametr nie zmienił się podczas tokenizacji. 

W celu zbadania jaka funkcja aproksymuje otrzymane punkty skorzystano z aproksymacji wielomianowej stopnia 2.

$a_1 \cdot x^2 + a_2 \cdot x + a_3$

W najlepszym przypadku otrzymane współczynniki $a_1$ i $a_3$ powinnny być jak najbliższe wartości 0, a wartość $a_2$ przybliżona wartości 1. 

# **Wyniki**
W folderze plots wstawione zostały wykresy z powyżej opisanej analizy. Poniżej przedstawiono wyniki liczbowe dla wartości $a_1$, $a_2$ i $a_3$. W folderze analysis znajduje się plik wykonawczy tokenizer_compare.py.

**Wyniki dla parametru end time**
| Tokenizator  | Współczynnik 1        | Współczynnik 2        | Współczynnik 3        |
|--------------|-----------------------|-----------------------|-----------------------|
| REMI         | -7.18481740e-07       | 9.90730898e-01        | -9.85569766e-01       |
| MIDILike     | -7.46241097e-07       | 9.90798380e-01        | -1.02440883e+00       |
| TSD          | -7.18481740e-07       | 9.90730898e-01        | -9.85569766e-01       |
| Structured   | -2.30054901e-05       | 1.02266682e+00        | -5.51502355e+00       |
| CPWord       | -7.18481740e-07       | 9.90730898e-01        | -9.85569766e-01       |
| MuMIDI       | -7.18481740e-07       | 9.90730898e-01        | -9.85569766e-01       |
| MMM          | -7.18481740e-07       | 9.90730898e-01        | -9.85569766e-01       |
| Octuple      | -7.18481740e-07       | 9.90730898e-01        | -9.85569766e-01       |

**Wyniki dla parametru estimated tempo**
| Tokenizator  | Współczynnik 1        | Współczynnik 2        | Współczynnik 3        |
|--------------|-----------------------|-----------------------|-----------------------|
| REMI         | 1.60749243e-02        | -5.92349227e+00       | 7.49900167e+02        |
| MIDILike     | 1.60749243e-02        | -5.92349227e+00       | 7.49900167e+02        |
| TSD          | 1.60749243e-02        | -5.92349227e+00       | 7.49900167e+02        |
| Structured   | 1.56814472e-02        | -5.87738582e+00       | 7.56469579e+02        |
| CPWord       | 1.60749243e-02        | -5.92349227e+00       | 7.49900167e+02        |
| MuMIDI       | 1.60749243e-02        | -5.92349227e+00       | 7.49900167e+02        |
| MMM          | 1.60749243e-02        | -5.92349227e+00       | 7.49900167e+02        |
| Octuple      | 1.60749243e-02        | -5.92349227e+00       | 7.49900167e+02        |

**Wyniki dla parametru file size**

| Tokenizator  | Współczynnik 1        | Współczynnik 2        | Współczynnik 3        |
|--------------|-----------------------|-----------------------|-----------------------|
| REMI         | 1.73317104e-07        | 6.51278294e-01        | 2.01919202e+03        |
| MIDILike     | 1.73275145e-07        | 6.51270699e-01        | 2.01991022e+03        |
| TSD          | 1.73317104e-07        | 6.51278294e-01        | 2.01919202e+03        |
| Structured   | 1.73299924e-07        | 6.51275883e-01        | 2.01926520e+03        |
| CPWord       | 1.73317104e-07        | 6.51278294e-01        | 2.01919202e+03        |
| MuMIDI       | -1.28295091e-07       | 2.16575665e+00        | 4.04088193e+03        |
| MMM          | 1.73317104e-07        | 6.51278294e-01        | 2.01919202e+03        |
| Octuple      | 1.73317104e-07        | 6.51278294e-01        | 2.01919202e+03        |


# **Analiza wyników**
Najmniejsze zmiany w pliku następowały dla parametru *end time*. Zgodnie z założeniami otrzymano pierwszy współczynnik bliski zeru, drugi współczynnik bliski wartości 1, natomiast trzeci jest przybliżony do wartości 1. Na wykresach można zaobserować wykres aproksymowany przybliżony do f(x) = x. Wykresy i wartości nie różnią się znacznie między tokenizatorami. 

Przy analizie *estimated tempo* można zaobserować, że wartości po tokenizacji znacznie odbiegają od wartości plików oryginalnych. Dodatkową obserwacją jest fakt, że funkcja prettyMIDI licząca ten parametr dla wszystkich tokenizatorów poza Structured zwróciła takie same wartości. Podczas odsłuchu plików po tokenizacji można zaobserować, że tempo jest w nich zaburzone, zwłaszcza przy bardzeij dynamicznych utworach. Dla przykładu w folderze MIDI files zamieszczono przykładowe pliki dla kilku tokenizatorów oraz plik oryginalny do porównania.

Analiza parametru *file size* wykazała, że dla tokenizatorów CPWord, MIDILike, MMM, Octuple, REMI
Structured, TSD nastąpiła kompresja pliku po tokenizacji. Wynika to z współczynnika nachylenia prostej aproksymującej dane wynikowe. Przeciwny efekt uzyskiwany jest tylko dla tokenizatora MuMIDI, który powiększył rozmiar pliku MIDI.


