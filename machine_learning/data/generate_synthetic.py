import pandas as pd
from typing import Literal, Optional
import numpy as np

LOWER_LIMIT = 5_000
UPPER_LIMIT = 10_000
np.random.seed(42)

def load_parameters(csv_path: str) -> pd.DataFrame:
    """
    Wczytaj parametry roczne do DataFrame i przygotuj do dalszego przetwarzania.
    """
    df = pd.read_csv(csv_path)
    # Usuń białe znaki z nazw kolumn
    df.columns = df.columns.str.strip()
    # Konwersja liczb zapisanych jako stringi z przecinkiem na float
    for col in [
        'średnioroczny wskaźnik cen towarów i usług konsumpcyjnych ogółem',
        'wskaźnik realnego wzrostu przeciętnego wynagrodzenia',
        'przeciętne miesięczne wynagrodzenie w gospodarce narodowej',
        'stopa składki na ubezpieczenie emerytalne finansowanej przez pracownika',
        'stopa składki na ubezpieczenie emerytalne finansowanej przez pracodawcę',
        'stopa składki na ubezpieczenie emerytalne odprowadzana do OFE',
        'stopa składki na ubezpieczenie emerytalne odprowadzana na subkonto',
        'łączna stopa składki odprowadzanej do OFE i składki ewidencjonowanej na subkoncie',
        'wskaźnik waloryzacji składek zewidencjonowanych na koncie oraz kapitału początkowego za dany rok',
        'wskaźnik waloryzacji składek zewidencjonowanych na subkoncie za dany rok',
        'ograniczenie górne miesięcznej podstawy wymiaru składek na ubezpieczenie emerytalne w danym roku, wyrażone w procencie przeciętnego miesięcznego wynagrodzenia w gospodarce narodowej',
        'kwota najniższej emerytury obowiązująca od marca danego roku do lutego następnego roku'
    ]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("\xa0", "")
            .str.replace(" ", "")
            .str.replace(",", ".")
            .str.replace("%", "")
            .str.replace('"', "")
            .replace("", "0")
            .astype(float)
        )
    df['rok'] = df['rok'].astype(int)
    df = df.set_index('rok')
    return df

# Funkcja do pobierania dzielnika (life expectancy) z pliku CSV
def get_dzielnik(year: int, age: int, csv_path: str = "Parametry-III 2025 - e_x M i K-PROGNOZA.csv") -> float:
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    # Usuwamy białe znaki i zamieniamy przecinki na kropki
    value = df.loc[df['wiek'] == age, str(year)].values
    if len(value) == 0:
        raise ValueError(f"Brak dzielnika dla wieku {age} i roku {year}")
    # Zamiana '1 001,2' na '1001.2'
    val = str(value[0]).replace('\xa0', '').replace(' ', '').replace(',', '.')
    return float(val)

def wylicz_emeryture(
    df: pd.DataFrame,
    plec: Literal["k", "m"],
    wynagrodzenie_brutto: float,
    rok_rozpoczecia: int,
    rok_zakonczenia: int,
    kapital_poczatkowy: float = 0.0,
    suma_wplaconych_skladek: float = 0.0,
    wiek: Optional[int] = None,
    absence: Optional[bool] = False,
    dzielnik_csv_path: str = "Parametry-III 2025 - e_x M i K-PROGNOZA.csv"
) -> dict:
    """
    Wylicza prognozowaną miesięczną emeryturę według ZUS, uwzględniając inflację i minimalną emeryturę.
    """
    # Dzielnik pobierany z tabeli na podstawie wieku i roku zakończenia
    # Przyjmujemy wiek emerytalny: wiek = 60 (k) lub 65 (m) jeśli nie podano
    if wiek is None:
        wiek = 60 if plec == "k" else 65
    dzielnik = get_dzielnik(rok_zakonczenia, wiek, csv_path=dzielnik_csv_path)

    konto = 0.0
    subkonto = 0.0
    suma_skladek = suma_wplaconych_skladek

    inflacja_cum = 1.0

    for rok in range(rok_rozpoczecia, rok_zakonczenia + 1):
        # Uwzględnij absencję chorobową i urlop macierzyński
        absence_days = 0.0
        if absence:
            # Dla kobiet: absencja + urlop macierzyński, dla mężczyzn tylko absencja
            absence_days = 15.92 if plec == "m" else (16.41 + 140.0)
        # Dla uproszczenia: 1 rok = 365 dni, więc procent roku bez składek:
        absence_factor = 1.0 - (absence_days / 365.0)
        params = df.loc[rok]

        pw = params['przeciętne miesięczne wynagrodzenie w gospodarce narodowej']
        limit = params['ograniczenie górne miesięcznej podstawy wymiaru składek na ubezpieczenie emerytalne w danym roku, wyrażone w procencie przeciętnego miesięcznego wynagrodzenia w gospodarce narodowej'] / 100
        min_emerytura = params['kwota najniższej emerytury obowiązująca od marca danego roku do lutego następnego roku']

        waloryzacja_konto = params['wskaźnik waloryzacji składek zewidencjonowanych na koncie oraz kapitału początkowego za dany rok'] / 100
        waloryzacja_subkonto = params['wskaźnik waloryzacji składek zewidencjonowanych na subkoncie za dany rok'] / 100

        inflacja = params['średnioroczny wskaźnik cen towarów i usług konsumpcyjnych ogółem'] / 100

        # Minimalna emerytura z roku przejścia na emeryturę
        min_emerytura = df.loc[rok_zakonczenia]['kwota najniższej emerytury obowiązująca od marca danego roku do lutego następnego roku']
    
        # Limit podstawy wymiaru składek
        max_podstawa = limit * pw
        podstawa = min(wynagrodzenie_brutto, max_podstawa)
        # Redukcja podstawy o absencję i urlop macierzyński
        podstawa *= absence_factor

        # Składki roczne
        skladka_konto = podstawa * 12 * (
            (params['stopa składki na ubezpieczenie emerytalne finansowanej przez pracownika']
             + params['stopa składki na ubezpieczenie emerytalne finansowanej przez pracodawcę'])/100
            - params['stopa składki na ubezpieczenie emerytalne odprowadzana na subkonto']/100
            - params['stopa składki na ubezpieczenie emerytalne odprowadzana do OFE']/100
        )
        skladka_subkonto = podstawa * 12 * (params['stopa składki na ubezpieczenie emerytalne odprowadzana na subkonto']/100)

        suma_skladek += skladka_konto + skladka_subkonto

        # Dodaj składki do kont
        konto += skladka_konto
        subkonto += skladka_subkonto

        # Waloryzacja kont
        konto *= waloryzacja_konto
        subkonto *= waloryzacja_subkonto

        # Waloryzacja kapitału początkowego (rok po roku)
        if kapital_poczatkowy > 0:
            kapital_poczatkowy *= waloryzacja_konto

        # Inflacja kumulowana (jako wskaźnik np. 1.025)
        inflacja_cum *= inflacja

    # Dodajemy ostateczny kapitał początkowy do konta
    konto += kapital_poczatkowy

    S = konto + subkonto
    emerytura_nominalna = S / dzielnik if dzielnik > 0 else 0.0

    lata_skladkowe = rok_zakonczenia - rok_rozpoczecia + 1
    
    # Zastosuj minimalną emeryturę tylko jeśli spełniony jest wymagany staż
    wymagany_staz = 20 if plec == "k" else 25
    if lata_skladkowe >= wymagany_staz:
        emerytura_nominalna = max(emerytura_nominalna, min_emerytura)

    # Minimalna emerytura z roku przejścia na emeryturę
    min_emerytura = df.loc[rok_zakonczenia]['kwota najniższej emerytury obowiązująca od marca danego roku do lutego następnego roku']
    emerytura_nominalna = max(emerytura_nominalna, min_emerytura)

    # Emerytura realna (w cenach z pierwszego roku pracy)
    emerytura_urealniona = emerytura_nominalna / inflacja_cum

    # Stopa zastąpienia względem przeciętnego wynagrodzenia w roku zakończenia pracy
    ostatnie_pw = df.loc[rok_zakonczenia]['przeciętne miesięczne wynagrodzenie w gospodarce narodowej']
    stopa_zastapienia = emerytura_nominalna / ostatnie_pw if ostatnie_pw else 0

    return {
        "emerytura_nominalna": emerytura_nominalna,
        "emerytura_urealniona": emerytura_urealniona,
        "stopa_zastapienia": stopa_zastapienia,
        "minimalna_emerytura": min_emerytura,
        "inflacja_cum": inflacja_cum,
        "konto": konto,
        "subkonto": subkonto,
        "S": S,
        "suma_skladek": suma_skladek
    }


def jest_zadowolony(df: pd.DataFrame):
    # Rozkład normalny przesunięty w lewo (łatwiej osiągnąć zadowolenie)
    prog = np.random.normal(
        loc=(LOWER_LIMIT + UPPER_LIMIT) / 2 * 0.8,  # średnia przesunięta w lewo
        scale=(UPPER_LIMIT - LOWER_LIMIT) / 6  # odchylenie standardowe
    )
    df['zadowolony'] = df['emerytura_nominalna'] > prog


# PRZYKŁAD UŻYCIA:
if __name__ == "__main__":
    import numpy as np
    df = load_parameters("Parametry-III 2025 - parametry roczne.csv")

    # Parametry losowania
    n = 10000  # liczba przykładów
    plec_options = ["k", "m"]

    # Funkcja do losowania z dużym priorytetem dla mniejszych wartości
    def skewed_low(a, b, size=1, skew=3):
        return (a + (b - a) * np.random.beta(skew, 1, size=size)).astype(int)

    # Funkcja do losowania z dużym priorytetem dla większych wartości
    def skewed_high(a, b, size=1, skew=3):
        return (a + (b - a) * np.random.beta(1, skew, size=size)).astype(int)

    results = []
    for _ in range(n):
        plec = np.random.choice(plec_options)
        wynagrodzenie_brutto = skewed_high(4500, 100000, skew=10)[0]
        rok_rozpoczecia = skewed_high(2024, 2064, skew=10)[0]
        rok_zakonczenia = skewed_low(rok_rozpoczecia+1, 2064, skew=5)[0]
        suma_wplaconych_skladek = skewed_high(0, 200000, skew=5)[0]
        absence = np.random.choice([True, False])

        wynik = wylicz_emeryture(
            df,
            plec=plec,
            wynagrodzenie_brutto=wynagrodzenie_brutto,
            rok_rozpoczecia=rok_rozpoczecia,
            rok_zakonczenia=rok_zakonczenia,
            kapital_poczatkowy=0,
            suma_wplaconych_skladek=suma_wplaconych_skladek,
            absence=absence
        )
        row = {
            "plec": plec,
            "wynagrodzenie_brutto": wynagrodzenie_brutto,
            "rok_rozpoczecia": rok_rozpoczecia,
            "rok_zakonczenia": rok_zakonczenia,
            "suma_wplaconych_skladek": suma_wplaconych_skladek,
            "emerytura_nominalna": wynik["emerytura_nominalna"]
        }
        results.append(row)
    
    df = pd.DataFrame(results)
    jest_zadowolony(df)
    df.to_csv("synthetic_data.csv", index=False)
    print(f"Zapisano {n} rekordów do synthetic_data.csv")