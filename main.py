import sys
from PyQt6.QtWidgets import QApplication, QWidget, QSlider, QDial, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class DialWithLabel(QWidget):
    """
    Composite widget that groups a QDial and a QLabel.
    The label always displays the current value of the dial.
    This widget provides a setValue method to update both the dial and the label together.
    """

    def __init__(self, min_val, max_val):
        """
        Initialize the dial and label, and set up the layout.

        Args:
            min_val (int): Minimum value for the dial.
            max_val (int): Maximum value for the dial.
        """
        super().__init__()
        self.dial = QDial()
        self.label = QLabel()

        # Configure dial
        self.dial.setNotchesVisible(True)
        self.dial.setRange(min_val, max_val)

        # Configure label
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Arrange widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.dial)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def setValue(self, value):
        """
        Set the value of the dial and update the label to match.

        Args:
            value (int): The value to set on the dial and display on the label.
        """
        self.dial.setValue(value)
        self.label.setText(f"Value: {value}")


class LinkedControlsApp(QWidget):
    """
    Main application window.
    Contains a QSlider and a DialWithLabel.
    Keeps both controls synchronized, so changing one updates the other.
    """

    def __init__(self):
        """
        Initialize the application window and controls.
        """
        super().__init__()
        self.current_value = 1  # Stores the current value shared by the slider and dial
        self.init_ui()

    def init_ui(self):
        """
        Set up the user interface, connect signals, and initialize control values.
        """
        layout = QVBoxLayout()

        # Create slider and composite dial-with-label widget
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.dial_widget = DialWithLabel(1, 10)

        # Set slider range to match the dial
        self.slider.setRange(1, 10)

        # Add widgets to the layout
        layout.addWidget(self.slider)
        layout.addWidget(self.dial_widget)
        self.setLayout(layout)

        # Connect valueChanged signals to the synchronization method
        self.slider.valueChanged.connect(self.set_current_value)
        self.dial_widget.dial.valueChanged.connect(self.set_current_value)

        # Set initial values for both controls
        self.slider.setValue(self.current_value)
        self.dial_widget.setValue(self.current_value)

    def set_current_value(self, value):
        """
        Synchronize the slider and dial so they always show the same value.
        Update the label in the dial widget as well.

        Args:
            value (int): The new value to set on both controls.
        """
        self.current_value = value

        # Determine which widget needs to be updated
        if self.sender() == self.slider:
            # If the slider was changed, update the dial widget
            widget = self.dial_widget
        else:
            # If the dial was changed, update the slider and the dial widget's label
            widget = self.slider
            self.dial_widget.setValue(value)

        # Prevent signal feedback loops while updating the other widget
        widget.blockSignals(True)
        widget.setValue(value)
        widget.blockSignals(False)


if __name__ == "__main__":
    # Standard PyQt application setup
    app = QApplication(sys.argv)
    window = LinkedControlsApp()
    window.setWindowTitle("Stateful Linked Controls")
    window.show()
    sys.exit(app.exec())