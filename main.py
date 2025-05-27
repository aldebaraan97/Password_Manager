import sys

from PyQt6.QtWidgets import QApplication
from PasswordGenerator1 import PasswordGenerator

def main():
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("Password Generator")

    # Create and show the main window
    window = PasswordGenerator()
    window.show()

    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()