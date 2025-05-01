import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySideGUI import MainWindow # Import the MainWindow class

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow() # Instantiate the MainWindow class
    window.show()
    sys.exit(app.exec())