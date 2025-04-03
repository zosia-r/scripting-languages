import os
import sys
from pathlib import Path

def process_path():
    path = os.environ.get("PATH")

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
        print("Script only accepts one parameter (-r)")

if __name__ == "__main__":
    process_path()

