Uproszczona implementacja tail -f
1 import time,sys,os
2
3 def tail(filename):
4 with open(filename, "r") as file:
5 # znajdujemy początkową pozycję pliku
6 file.seek(0)
7 while True:
8 # zapisujemy aktualną pozycję pliku
9 current_position = file.tell()
10 line = file.readline()
11 if not line:
12 # jeśli nie ma nowych linii, czekamy chwilę
13 time.sleep(0.1)
14
15 # weryfikujemy rozmiar pliku
16 current_size = os.stat(filename).st_size
17
18 # jeśli obecna pozycja jest dalej,
19 # niż rozmiar pliku, przesuwamy na początek
20 if current_position > current_size:
21 file.seek(0)
22 else:
23 # jeśli mamy nową linię, wypisujemy ją na ekran
24 sys.stdout.write(line)
25 sys.stdout.flush()
26
27 if __name__ == "__main__":
28 try:
29 tail(sys.argv[1])
30 except IndexError:
31 print("Please provide first argument.")