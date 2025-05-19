import pandas as pd
import math as math
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'



# PRZYGOTOWANIE DANYCH

# Wczytanie danych z Excela jako dataframe
file = 'dane.xlsx'
# file = 'dane2.xls'
xl = pd.ExcelFile(file)
data = xl.parse('Arkusz1')

# Przygotowane do wczytywania dla dowolnych danych
# przeslanki = []
# l_przeslanek = int(input("Podaj liczbę przesłanek: "))
# przeslanki_dl = []
# for i in range(0,l_przeslanek):
#     przeslanka = input("Podaj nazwę przeslanki nr " + str(i+1) + ": ")
#     l_atrybutow = int(input("Podaj liczbę atrybutów w przesłance " + str(i+1) + ": "))
#     przeslanki.append(przeslanka)
#     przeslanki_dl.append(l_atrybutow)
#
# l_wartosci=int(input("Podaj liczbę możliwych wartości w konkluzji: "))
# konkluzja = input("Podaj nazwę konkluzji")

# Przygotowanie pod konkretne dane w projekcie
l_przeslanek = 5 # Liczba przesłanek
przeslanki_dl = [4, 4, 3, 2, 3] # Tablica z liczbą atrybutów dla poszczególnych przesłanek
przeslanki = ["Wiek", "Z kim ogladasz", "Humor", "Plec", "Oczekiwania"] # Tablica z nazwami przeslanek
l_wartosci = 5 # Liczba mozliwych wartości w konkluzji
konkluzja = "Film" # Nazwa konkluzji

suma = l_wartosci # suma kolumn w zbiorze danych
for i in przeslanki_dl:
    suma += i

# Usuwanie niepotrzebnych kolumn powstając przy wczytaniu
columns = list(data)
for i in range(suma, len(columns)):
    data.drop(columns[i], axis=1, inplace=True)
columns = columns[0:suma]



# PROGRAM - BINANRNE DRZEWA DECYZYJNE

# Graficzna prezentacja wyniku - drzewo decyzyjne

# Rozpoczęcie drzewa
tree = Digraph('Jaki film wybrać?', filename='tree.gv')

# tablica pomocnicza sprawdzająca czy dana przesłanka już się pojawiła (Na potrzeby graficznej wizualizacji - sprawia , że drzewo jest czytelniejsze)
czy_przeslanka = []
for i in range(0, suma-l_wartosci):
    czy_przeslanka.append(0)
# Tablica pomocnicza nadająca kolejnym konkluzjom indexy (Również na potrzeby graficznej prezentacji)
index_konkluzji = []
index_konkluzji.append(0)


# Funkcja wywołująca się po stwierdzeniu że potwierdzenie/zaprzeczenie warunku jednoznacznie wskazuje na jakąś konkluzję
def jednoznaczne(ktora_przeslanka, ktory_index, tak_nie, konkluzja):
        index_konkluzji[0] += 1
        print("Wynik jednoznaczny: " + konkluzja + " dla: " + tak_nie + ": " + przeslanki[ktora_przeslanka] + ": " + columns[ktory_index])
        # Graficzna reprezentacja tego, że dana przesłanka jednoznacznie wskazuje na daną konkluzję
        tree.edge("(" + str(czy_przeslanka[ktory_index]) + ") " + przeslanki[ktora_przeslanka] + " - " + columns[ktory_index], "(" + str(index_konkluzji[0]) + ") " + konkluzja, label=tak_nie)


# Główna funkcja programu - dzieląca tabelę na 2
def podziel(data, ktora_przeslanka, ktory_index, poczatek_drzewa, tak_nie):

    print("\n\n\n\n---------POCZATEK PETLI---------------\n")

    data = data.reset_index(drop=True) # Reset indexu (potrzebny dla kolejnych przejsc funkcji)

    czy_przerwac = 0
    N = len(data[columns[0]])  # liczba wszystkich kombinacji
    Konkluzja_n = []  # Tablica z ni dla poszczególnych wartości konkluzji
    for i in range(suma - l_wartosci, suma):
        suma_pom = 0
        for j in data[columns[i]]:
            suma_pom += j
        Konkluzja_n.append(suma_pom)
        if(suma_pom == N):
            czy_przerwac = 1
            # Jeżeli zsumowane wartości dla warunku są równe liczbie wszystkich kombinacji to znaczy, że ten warunek gwarantuje ten wynik
            suma_pom_2=0
            for x2 in data[columns[ktory_index]]:
                suma_pom_2 += x2
            if suma_pom_2 == 0:
                jednoznaczne(ktora_przeslanka, ktory_index, "nie", columns[i])
            else:
                jednoznaczne(ktora_przeslanka, ktory_index, "tak", columns[i])
            break

    if czy_przerwac == 0:
        # Obliczanie I : Entropii dla wartości konkluzji
        I = 0
        I_j = []  # Tablica przechowujaca poszczegolne wartosci entropii dla różnych konkluzji
        for ni in Konkluzja_n:
            if(ni != 0):
                E = -(ni / N) * math.log((ni / N), 2)
                I_j.append(E)
            else:
                E = 0
                I_j.append(E)
            I += E


        # Obliczanie Entropii dla warunków
        tab_I_j_plus = []
        tab_I_j_minus = []
        tab_E_j = []
        tab_I_minus_E = []  # Tablica z której na podstawie max(I-Ej) jest wybierany warunek do dzielenia tabeli
        for j in range(0, suma - l_wartosci):

            # 1) Entropia po potwierdzeniu warunku (Obliczanie Ij+)
            nj_plus = 0
            for i in data[columns[j]]:
                nj_plus += i

            # k - odnosi się do numeru klasy - czyli numeru wartości konkluzji
            tab_Xj_plus_k = []
            for k in range(0, l_wartosci):
                nj_plus_k = 0;
                for i in range(0, len(data[columns[j]])):
                    if (data[columns[j]][i] == 1 and data[columns[suma - l_wartosci + k]][i] == 1):
                        nj_plus_k += 1

                if (nj_plus_k == 0):
                    Xj_plus_k = 0
                else:
                    Xj_plus_k = -(nj_plus_k / nj_plus) * math.log((nj_plus_k / nj_plus), 2)

                tab_Xj_plus_k.append(Xj_plus_k)

            I_j_plus = 0  # Entropia po potwierdzeniu warunku j
            for x in tab_Xj_plus_k:
                I_j_plus += x

            tab_I_j_plus.append(I_j_plus)

            # 2) Entropia po zaprzeczeniu warunku (Obliczanie Ij-)
            nj_minus = 0;
            for i in data[columns[j]]:
                if (i == 0):
                    nj_minus += 1

            # k - odnosi się do numeru klasy - czyli numeru wartości konkluzji
            tab_Xj_minus_k = []
            for k in range(0, l_wartosci):
                nj_minus_k = 0;
                for i in range(0, len(data[columns[j]])):
                    if (data[columns[j]][i] == 0 and data[columns[suma - l_wartosci + k]][i] == 1):
                        nj_minus_k += 1

                if (nj_minus_k == 0):
                    Xj_minus_k = 0
                else:
                    Xj_minus_k = -(nj_minus_k / nj_minus) * math.log((nj_minus_k / nj_minus), 2)

                tab_Xj_minus_k.append(Xj_minus_k)

            I_j_minus = 0  # Entropia po potwierdzeniu warunku j
            for x in tab_Xj_minus_k:
                I_j_minus += x

            tab_I_j_minus.append(I_j_minus)

            # Obliczenia dla Entropii po ocenie całego warunku
            E_j = (nj_plus / N) * I_j_plus + (nj_minus / N) * I_j_minus
            tab_E_j.append(E_j)
            tab_I_minus_E.append(I - E_j)

        # print(tab_I_j_plus)
        # print(tab_I_j_minus)
        # print(tab_E_j)
        # print(tab_I_minus_E)

        index = tab_I_minus_E.index(max(tab_I_minus_E)) #index (w tabeli) wartości przesłanki, na podstawie której będzimey dzielić tabelę

        # Przypadek w którym cała tablica I - E zawiera same 0 (Ponieważ funkcja max wybiera w tym wypadku zawsze element o indeksie 0)
        # Wybieramy tutaj pierwszą napotkaną w tablicy wartość przesłanki która ma różne wartości (nie same zera i nie same jedynki)
        suma_pom_0 = 0
        for x in tab_I_minus_E:
            suma_pom_0 += x
        if suma_pom_0 == 0:
            for i in range(0, suma-l_wartosci):
                suma_pom_1 = 0
                for x2 in data[columns[i]]:
                    suma_pom_1 += x2
                if(suma_pom_1 != 0 and suma_pom_1 != len(data[columns[i]])):
                    index = i
                    break


        # Ktora to przeslanka? - petla sprawdzajaca jaka jest ogólna nazwa przeslanki dla indexu (Na potrzeby wyświetlania informacji)
        ktora = -1
        pom = 0
        for i in range(0, len(przeslanki_dl)):
            if (index < przeslanki_dl[i] + pom):
                ktora = i
                break
            else:
                pom += przeslanki_dl[i]


        print("Tabelę dzielimy dla przesłanki: " + przeslanki[ktora] + ": " + columns[index])

        # Podział tabeli
        data1 = data[data[columns[index]] != 0]  # Tabela dla potwierdzonego warunku - wartosc 1
        data2 = data[data[columns[index]] != 1]  # Tabela dla zaprzeczonego warunku - wartosc 0
        data1 = data1.reset_index(drop=True) # Reset indexu
        data2 = data2.reset_index(drop=True) # Reset indexu

        print("Dlugosc tabeli 1: " + str(len(data1[columns[0]])))
        print("Dlugosc tabeli 2: " + str(len(data2[columns[0]])))

        # Update tablicy przechowujacej informacje czy dana przeslanka juz sie pojawila (na potrzeby graficznej prezentacji)
        czy_przeslanka[index] = czy_przeslanka[index]+1

        # Graficzna przezentacja drzewa
        if poczatek_drzewa == 0:
            tree.edge('Jaki film wybrać?', "(" +  str(czy_przeslanka[index]) + ") " + przeslanki[ktora] + " - " + columns[index])
        else:
            tree.edge("(" + str(czy_przeslanka[ktory_index]) + ") " +  przeslanki[ktora_przeslanka] + " - " + columns[ktory_index], "(" + str(czy_przeslanka[index]) + ") " +  przeslanki[ktora] + " - " + columns[index], label=tak_nie)

        # Warunki dalszego zachowania programu:
        # Jeżeli oba datasety mają długość 1 to oznacza że w jednym warunek potwierdzający bezpośrednio wskazuje na konkluzję,
        # a w drugim warunek zaprzeczający bezpośrednio wskazuje na konkluzję.
        # Wyniki przekazujemy do funkcji "jednoznacznie" w tym momencie ponieważ przekazanie dataframeu o długości 1
        # Do dalszej funkcji powoduje zaburzenie działania programu (Oba warunki są postrzegane jako potwierdzające)
        if len(data1[columns[0]]) == 1 and len(data2[columns[0]]) == 1:
            konkluzja = ""
            for z in range(suma - l_wartosci, suma):
                if data1[columns[z]][0] == 1:
                    konkluzja = columns[z]
                    break
            jednoznaczne(ktora, index, "tak", konkluzja)
            konkluzja = ""
            for z in range(suma - l_wartosci, suma):
                if data2[columns[z]][0] == 1:
                    konkluzja = columns[z]
                    break
            jednoznaczne(ktora, index, "nie", konkluzja)
        else:
            # Przypadek w którym jedna z kolumn ma długość 0, przekazujemy do podziału tylko tą drugą
            if len(data1[columns[0]]) == 0 or len(data2[columns[0]]) == 0:
                if(len(data1[columns[0]]) != 0):
                    podziel(data1, ktora, index, 1, "nie")
                else:
                    podziel(data2, ktora, index, 1, "nie")
            else:
                # Żaden z powyższych warunków specjalnych nie jest spełniony - przekazujemy oba datasety dalej
                podziel(data1, ktora, index, 1, "tak") #Przekazanie datatsetu dla którego warunek = 1
                podziel(data2, ktora, index, 1, "nie") #Przekazanie datatsetu dla którego warunek = 0

podziel(data, 0, 0, 0, "tak")
print(tree.source)
tree.view()


