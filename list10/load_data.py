import sqlite3
import sys
import csv
import os

def get_station_id(cursor, station_name):
    if not station_name or station_name.strip() == "" or station_name.lower() == "poza stacją" or station_name.lower() == "poza stacjÄ…":
        return None

    cursor.execute("SELECT id FROM stations WHERE name = ?", (station_name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute("INSERT INTO stations (name) VALUES (?)", (station_name,))
        return cursor.lastrowid

def load_data(csv_file, db_name):
    db_file = f"{db_name}.sqlite3"
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' does not exist.")
        return
    if not os.path.exists(db_file):
        print(f"Error: Database file '{db_file}' does not exist.")
        return

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    inserted_count = 0

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            try:
                uid = int(row['UID wynajmu'])
                bike_number = int(row['Numer roweru'])
                start_time = row['Data wynajmu']
                end_time = row['Data zwrotu']
                start_station_name = row['Stacja wynajmu']
                end_station_name = row['Stacja zwrotu']
                duration = int(row['Czas trwania'])

                start_station_id = get_station_id(cursor, start_station_name)
                end_station_id = get_station_id(cursor, end_station_name)

                cursor.execute('''
                    INSERT OR IGNORE INTO rentals 
                    (uid, bike_number, start_time, end_time, start_station_id, end_station_id, duration)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (uid, bike_number, start_time, end_time, start_station_id, end_station_id, duration))

                inserted_count += 1
            except Exception as e:
                print(f"Error inserting row {row}: {e}")

    connection.commit()
    connection.close()
    print(f"Inserted {inserted_count} records to the data base '{db_file}' from file '{csv_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python load_data.py <csv_file> <db_name>")
    else:
        csv_file = sys.argv[1]
        db_name = sys.argv[2]
        load_data(csv_file, db_name)
