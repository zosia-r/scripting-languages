import re
from pathlib import Path


def group_measurement_files_by_key(path):
    pattern = re.compile(r"^(19\d{2}|20[0-2][0-5])_([\w\s\d\-\(\)]+)_([0-9]+[HhDdGgYy])\.csv$")
    # ^ i $ = początek i koniec
    # (19\d{2}|20[0-2]\d) = rok 1900-2025
    # [\w\s\d\-\(\)]+ = parametr (litery, cyfry, spacje, myślniki, nawiasy)
    # [0-9]+[HhDdGgYy] = częstotliwość (cyfry + jednostka)
    # \.csv$ = końcówka .csv

    dict = {}

    for file in path.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match:
                key = (match.group(1), match.group(2), match.group(3))
                dict[key] = file.name

    return dict



if __name__ == "__main__":
    path = Path('measurements')

    if not path.exists():
        print(f"Folder {path} nie istnieje!")
        exit()
    
    print("Pliki w folderze:")
    for file in path.iterdir():
        if file.is_file():
            print(f" - {file.name}")

    grouped_files = group_measurement_files_by_key(path)

    print(f"\nZnaleziono pasujące pliki: {len(grouped_files)}")

    for key, file in grouped_files.items():
        print(f"{key}: {file}")