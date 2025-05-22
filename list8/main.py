import sys
from PySide6.QtWidgets import QApplication
from gui import LogViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogViewer()
    window.show()
    sys.exit(app.exec())