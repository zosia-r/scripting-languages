import sys,time,os,io
from collections import deque

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def process_lines(source, n):
    lines = deque(source, maxlen=n)
    for line in lines:
        sys.stdout.write(line)
    sys.stdout.flush()

def follow(file):
    while True:
        line = file.readline()
        if line:
            sys.stdout.write(line)
            sys.stdout.flush()
        else:
            time.sleep(0.1)  # Czekamy na nowe linie

def tail(filename, n, to_follow):
    try:
        with open(filename, "r", encoding='utf-8') as file:
            process_lines(file, n)  # Wyświetlamy ostatnie n linii 
            if to_follow: follow(file)
    except Exception as e:
        print(f"Error: {e}")

def parse_arguments():
    filename = None
    n = 10
    to_follow = False
    
    for arg in sys.argv[1:]:
        if arg.startswith("--lines="):
            try:
                n = int(arg.split("=")[1])
            except ValueError:
                print("Invalid number of lines.")
                sys.exit(1)
        elif arg == "--follow":
            to_follow = True
        else:
            filename = arg
    return filename, n, to_follow

if __name__ == "__main__":
    filename, n, to_follow = parse_arguments()

    if filename:
        tail(filename, n, to_follow)
    else:
        process_lines(sys.stdin, n)
