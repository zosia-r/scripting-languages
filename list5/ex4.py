import re
from pathlib import Path
from ex1 import parse_stations

date_pattern = re.compile(r'^(19\d{2}|20[0-2][0-5])-(0[1-9]|1[0-2])-([0-2]\d|3[0-1])$')
coord_pattern = re.compile(r'^\d\.\d{6}$')
dash_pattern= re.compile(r'.+-.+')
triple_pattern = re.compile(r'[^-]+-[^-]+-[^-]+')
pattern_comma_street = re.compile(r",.*\b(ul\.|al\.)")

polish_map = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l',
            'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z',
            'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L',
            'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z',
            'Ż': 'Z'
        }




def extract_dates(path):
    dates = set()
    stations = parse_stations(path.name)

    for data in stations.values():
        date1 = data.get('Data uruchomienia', '')
        date2 = data.get('Data zamknięcia', '')
        if date_pattern.match(date1):
            dates.add(date1)
        if date_pattern.match(date2):
            dates.add(date2)

    return dates


def extract_coordinates(path):
    coords = []
    stations = parse_stations(path.name)

    for data in stations.values():
        n = data.get('WGS84 φ N', '')
        e = data.get('WGS84 λ E', '')
        if coord_pattern.match(n) and coord_pattern.match(e):
            coords.append((float(n), float(e)))

    return coords


def stations_with_dash(path):
    dashed_names = []
    stations = parse_stations(path.name)

    for data in stations.values():
        name = data.get('Nazwa stacji', '')
        if dash_pattern.match(name):
            dashed_names.append(name)

    return dashed_names


def normalize_station_names(path: Path):
    def replace_polish_chars(text):
        return ''.join(polish_map.get(c, c) for c in text)
    
    normalized = []
    stations = parse_stations(path.name)

    for data in stations.values():
        name = data.get('Nazwa stacji', '')
        name_underscore = name.replace(' ', '_')
        name_ascii = replace_polish_chars(name_underscore)
        normalized.append(name_ascii)

    return normalized



def verify_mob_stations(path: Path):
    bad_codes = []
    stations = parse_stations(path.name)

    for data in stations.values():
        code = data.get('Kod stacji', '').upper()
        type = data.get('Rodzaj stacji', '').upper().strip()
        if code.endswith("MOB") and type != "MOBILNA":
                bad_codes.append(code)

    return bad_codes


def three_part_locations(path: Path):
    matches = []
    stations = parse_stations(path.name)

    for data in stations.values():
        name = stations.get('Nazwa stacji', '')
        if triple_pattern.match(name):
            matches.append(name)
    return matches


def locations_with_comma_and_street(path: Path):
    results = []
    stations = parse_stations(path.name)

    for data in stations.values():
        address = data.get('Adres', '')
        if pattern_comma_street.match(address):
            results.append(address)

    return results



if __name__ == "__main__":
    path = Path("stacje.csv")
    print("Daty: ", extract_dates(path))
    print("Współrzędne: ", extract_coordinates(path))
    print("Nazwy z myślnikiem: ", stations_with_dash(path))
    print("Nazwy stacji po normalizacji: ", normalize_station_names(path))
    print("Stacje MOB, które nie są mobilne: ", verify_mob_stations(path))
    print("Lokalizacje 3-członowe oddzielone myślnikiem: ", three_part_locations(path))
    print("Lokalizacje zawierające przecinek i ul. lub al.: ", locations_with_comma_and_street(path))