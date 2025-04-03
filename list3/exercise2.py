import os
import sys
from pathlib import Path

path = os.environ.get("PATH")  # Pobiera wartość zmiennej PATH

path = path.split(";")
arguments = sys.argv[1:]

if len(arguments) == 0: 
    for p in path: 
        if p != "": print(p)
elif len(arguments) == 1 and arguments[0] == "-r":
    for p in path:
        print(p)
        for file in Path(p).iterdir():
            if file.is_file():
                print(" - " + str(file))
else:
    print("script only accepts one parameter (-r)")

