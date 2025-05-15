import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("PyQt6 Hello World")
        self.setGeometry(100, 100, 400, 200)  # x, y, width, height

        # Create a label with text
        label = QLabel("Hello World!")

        # Set font size for better visibility
        font = label.font()
        font.setPointSize(20)
        label.setFont(font)

        # Create layout and add label
        layout = QVBoxLayout()
        layout.addWidget(label)

        # Center the label in the layout
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Apply layout to the window
        self.setLayout(layout)


if __name__ == '__main__':
    # Create the application
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the event loop
    sys.exit(app.exec())