import pandas as pd
from typing import Literal, Optional

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
def wylicz_emeryture(
    df: pd.DataFrame,
    plec: Literal["k", "m"],
    wynagrodzenie_brutto: float,
    rok_rozpoczecia: int,
    rok_zakonczenia: int,
    kapital_poczatkowy: float = 0.0,
    wiek: Optional[int] = None,  # niewykorzystywane w tym uproszczeniu
) -> dict:
    """
    Wylicza prognozowaną miesięczną emeryturę według ZUS, uwzględniając inflację i minimalną emeryturę.

    Args:
        df (pd.DataFrame): DataFrame z parametrami rocznymi.
        plec (Literal["k", "m"]): Płeć użytkownika ("k" - kobieta, "m" - mężczyzna).
        wynagrodzenie_brutto (float): Obecne miesięczne wynagrodzenie brutto.
        rok_rozpoczecia (int): Rok rozpoczęcia pracy.
        rok_zakonczenia (int): Rok zakończenia pracy.
        kapital_poczatkowy (float): Kapitał początkowy (dla osób pracujących przed 1999).
        wiek (Optional[int]): Obecny wiek użytkownika (opcjonalnie).

    Returns:
        dict: Słownik z wynikami: emerytura nominalna, urealniona, stopa zastąpienia, min emerytura, itd.
    """
    # Stały dzielnik wg płci (miesiące)
    dzielnik = 987 if plec == "k" else 899

    konto = 0.0
    subkonto = 0.0

    # Używamy domyślnie podziału: konto = 9,76% - OFE - subkonto; subkonto = 4,38%
    for rok in range(rok_rozpoczecia, rok_zakonczenia + 1):
        params = df.loc[rok]
        pw = params['przeciętne miesięczne wynagrodzenie w gospodarce narodowej']
        limit = params['ograniczenie górne miesięcznej podstawy wymiaru składek na ubezpieczenie emerytalne w danym roku, wyrażone w procencie przeciętnego miesięcznego wynagrodzenia w gospodarce narodowej'] / 100
        min_emerytura = params['kwota najniższej emerytury obowiązująca od marca danego roku do lutego następnego roku']
        inflacja = params['średnioroczny wskaźnik cen towarów i usług konsumpcyjnych ogółem']
        waloryzacja_konto = params['wskaźnik waloryzacji składek zewidencjonowanych na koncie oraz kapitału początkowego za dany rok'] / 100
        waloryzacja_subkonto = params['wskaźnik waloryzacji składek zewidencjonowanych na subkoncie za dany rok'] / 100

        # Limit składek: podstawa = min(wynagrodzenie_brutto, limit * pw)
        max_podstawa = limit * pw
        podstawa = min(wynagrodzenie_brutto, max_podstawa)

        # Składka roczna = podstawa * 12 * odpowiednia stopa
        skladka_konto = podstawa * 12 * ((params['stopa składki na ubezpieczenie emerytalne finansowanej przez pracownika'] + params['stopa składki na ubezpieczenie emerytalne finansowanej przez pracodawcę'])/100 - params['stopa składki na ubezpieczenie emerytalne odprowadzana na subkonto']/100 - params['stopa składki na ubezpieczenie emerytalne odprowadzana do OFE']/100)
        skladka_subkonto = podstawa * 12 * (params['stopa składki na ubezpieczenie emerytalne odprowadzana na subkonto']/100)
        # OFE nie uwzględniamy, bo środki trafiają potem na subkonto

        # Waloryzacja składek i sumowanie
        konto = (konto + skladka_konto) * waloryzacja_konto
        subkonto = (subkonto + skladka_subkonto) * waloryzacja_subkonto

    # Dodajemy kapitał początkowy (waloryzowany)
    # Przyjmujemy, że waloryzacja kapitału = waloryzacja ostatniego roku pracy
    if kapital_poczatkowy > 0:
        konto += kapital_poczatkowy * waloryzacja_konto

    S = konto + subkonto
    emerytura_nominalna = S / dzielnik if dzielnik > 0 else 0.0

    # Minimalna emerytura – z roku przejścia na emeryturę!
    min_emerytura = df.loc[rok_zakonczenia]['kwota najniższej emerytury obowiązująca od marca danego roku do lutego następnego roku']
    emerytura_nominalna = max(emerytura_nominalna, min_emerytura)

    # Urealnienie – mnożymy przez iloczyn (1/inflacja) z lat od przejścia na emeryturę do dziś (lub odwrotnie, w zależności od celu)
    # Tu: pokazujemy siłę nabywczą świadczenia w cenach z pierwszego roku pracy
    inflacja_cum = 1.0
    for rok in range(rok_rozpoczecia, rok_zakonczenia + 1):
        inflacja_cum *= df.loc[rok]['średnioroczny wskaźnik cen towarów i usług konsumpcyjnych ogółem']
    emerytura_urealniona = emerytura_nominalna / inflacja_cum

    # Stopa zastąpienia względem ostatniego wynagrodzenia
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
        "S": S
    }

# PRZYKŁAD UŻYCIA:
if __name__ == "__main__":
    df = load_parameters("Parametry-III 2025 - parametry roczne.csv")
    wynik = wylicz_emeryture(
        df,
        plec="m",
        wynagrodzenie_brutto=8000,
        rok_rozpoczecia=2024,
        rok_zakonczenia=2064,
        kapital_poczatkowy=0
    )
    print(wynik)