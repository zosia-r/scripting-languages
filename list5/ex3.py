from ex1 import parse_stations
from pathlib import Path
import re

def get_addresses(path, city):
    pattern = re.compile(r'ul\.\s*([\w\s\-]+?)(?:[,\s]+(\d+\w?))?$')
    # ul\. = ul.
    # \s* = zero lub więcej spacji
    # ([\w\s\-]+?) = nazwa ulicy (litery, spacje, myślniki)
    # (?:[,\s]+(\d+\w?))? = numer ulicy (opcjonalny), może być z literą na końcu

    addresses = []

    stations = parse_stations(path.name)

    for data in stations.values():
        if data['Miejscowość'].strip().lower() == city.strip().lower():
            voiv = data.get('Województwo', '')
            city = data.get('Miejscowość', '')
            address = data.get('Adres', '')

            match = pattern.search(address)
            if match:
                    ulica = match.group(1).strip()
                    if match.group(2):
                        numer = match.group(2).strip()
                        addresses.append((voiv, city, ulica, numer))
                    else:
                        addresses.append((voiv, city, ulica, None))

    return addresses



if __name__ == "__main__":
    path = Path("stacje.csv")
    city = "Wrocław"
    wynik = get_addresses(path, city)
    print(wynik)