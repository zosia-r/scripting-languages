from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget,
    QLabel, QHBoxLayout, QFileDialog, QDateTimeEdit
)
from PySide6.QtCore import Qt, QDateTime
from datetime import datetime
from log_parser import load_log_file
from log_browser import LogBrowser

class LogViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Przeglądarka logów HTTP")
        self.resize(900, 500)

        self.browser = None

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        # Wczytywanie pliku
        load_btn = QPushButton("Wczytaj plik z logami")
        load_btn.clicked.connect(self.load_logs)
        layout.addWidget(load_btn)

        # Filtrowanie dat
        date_layout = QHBoxLayout()
        self.date_from = QDateTimeEdit()
        self.date_from.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_to = QDateTimeEdit()
        self.date_to.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        filter_btn = QPushButton("Zastosuj filtr")
        filter_btn.clicked.connect(self.apply_filter)
        date_layout.addWidget(self.date_from)
        date_layout.addWidget(self.date_to)
        date_layout.addWidget(filter_btn)
        layout.addLayout(date_layout)

        # Widok master-detail
        view_layout = QHBoxLayout()
        self.log_list = QListWidget()
        self.log_list.currentRowChanged.connect(self.update_details)
        view_layout.addWidget(self.log_list)

        self.detail_labels = {
            'uid': QLabel(),
            'timestamp': QLabel(),
            'method': QLabel(),
            'uri': QLabel(),
            'status_code': QLabel(),
            'origin_host': QLabel(),
            'origin_port': QLabel(),
            'destination_host': QLabel(),
            'destination_port': QLabel(),
            'host_domain': QLabel(),
        }

        detail_widget = QVBoxLayout()
        for label in self.detail_labels.values():
            detail_widget.addWidget(label)
        view_layout.addLayout(detail_widget)

        layout.addLayout(view_layout)

        # Nawigacja
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Poprzedni")
        self.next_btn = QPushButton("Następny")
        self.prev_btn.clicked.connect(self.previous_log)
        self.next_btn.clicked.connect(self.next_log)
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        layout.addLayout(nav_layout)

        self.update_navigation()

    def load_logs(self):
        path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik z logami")
        if path:
            entries = load_log_file(path)
            self.browser = LogBrowser(entries)
            self.update_log_list()

    def update_log_list(self):
        self.log_list.clear()
        for log in self.browser.filtered_logs:
            text = log.raw[:60] + "..."
            self.log_list.addItem(text)
        self.update_navigation()
        self.log_list.setCurrentRow(0)

    def update_details(self, index):
        log = self.browser.current_log()
        if not log:
            return
        
        self.detail_labels['timestamp'].setText(f"Czas: {datetime.fromtimestamp(log.timestamp)}")
        self.detail_labels['uid'].setText(f"UID: {log.uid}")
        self.detail_labels['method'].setText(f"Metoda: {log.method}")
        self.detail_labels['uri'].setText(f"URI: {log.uri}")
        self.detail_labels['status_code'].setText(f"Status: {log.status_code}")
        self.detail_labels['origin_host'].setText(f"Host źródłowy: {log.origin_host}")
        self.detail_labels['origin_port'].setText(f"Port źródłowy: {log.origin_port}")
        self.detail_labels['destination_host'].setText(f"Host docelowy: {log.destination_host}")
        self.detail_labels['destination_port'].setText(f"Port docelowy: {log.destination_port}")
        self.detail_labels['host_domain'].setText(f"Domena docelowa: {log.host_domain}")

        self.update_navigation()

    def apply_filter(self):
        if self.browser:
            start = self.date_from.dateTime().toPython()
            end = self.date_to.dateTime().toPython()
            self.browser.filter_by_time(start, end)
            self.update_log_list()

    def next_log(self):
        if self.browser and self.browser.has_next():
            self.browser.next_log()
            self.log_list.setCurrentRow(self.browser.current_index)

    def previous_log(self):
        if self.browser and self.browser.has_previous():
            self.browser.previous_log()
            self.log_list.setCurrentRow(self.browser.current_index)

    def update_navigation(self):
        if not self.browser:
            self.prev_btn.setDisabled(True)
            self.next_btn.setDisabled(True)
        else:
            self.prev_btn.setDisabled(not self.browser.has_previous())
            self.next_btn.setDisabled(not self.browser.has_next())
