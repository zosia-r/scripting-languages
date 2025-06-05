import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox,
    QPushButton, QLabel, QMessageBox
)

DB_NAME = "rentals.sqlite3"

class StationStatsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Station Statistics")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.station_combo = QComboBox()
        self.layout.addWidget(QLabel("Select a station:"))
        self.layout.addWidget(self.station_combo)

        self.load_stations()

        self.fetch_button = QPushButton("Show Statistics")
        self.fetch_button.clicked.connect(self.show_stats)
        self.layout.addWidget(self.fetch_button)

        self.results_label = QLabel("")
        self.results_label.setWordWrap(True)
        self.layout.addWidget(self.results_label)

    def load_stations(self):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM stations ORDER BY name ASC")
                self.stations = cursor.fetchall()
                for station in self.stations:
                    self.station_combo.addItem(station[1], station[0])
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def show_stats(self):
        station_id = self.station_combo.currentData()
        station_name = self.station_combo.currentText()

        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()

                # a. Average duration of rides starting from the station
                cursor.execute("SELECT AVG(duration) FROM rentals WHERE start_station_id = ?", (station_id,))
                avg_start = cursor.fetchone()[0]

                # b. Average duration of rides ending at the station
                cursor.execute("SELECT AVG(duration) FROM rentals WHERE end_station_id = ?", (station_id,))
                avg_end = cursor.fetchone()[0]

                # c. Number of unique bikes parked at this station
                cursor.execute("SELECT COUNT(DISTINCT bike_number) FROM rentals WHERE end_station_id = ?", (station_id,))
                unique_bikes = cursor.fetchone()[0]

                # d. Custom query: rides that start and end at the same station
                cursor.execute("""
                    SELECT COUNT(*) FROM rentals 
                    WHERE start_station_id = ? AND end_station_id = ?
                """, (station_id, station_id))
                same_station_rides = cursor.fetchone()[0]

            # Display results
            result_text = f"""
<b>Statistics for: {station_name}</b><br><br>
1. Average duration of rides starting here: <b>{round(avg_start or 0, 2)}</b> minutes<br>
2. Average duration of rides ending here: <b>{round(avg_end or 0, 2)}</b> minutes<br>
3. Unique bikes parked here: <b>{unique_bikes}</b><br>
4. Rides that started and ended at this station: <b>{same_station_rides}</b>
"""
            self.results_label.setText(result_text)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StationStatsApp()
    window.show()
    sys.exit(app.exec_())
