from PyQt6.QtCore import QObject, pyqtSignal


class Counter(QObject):
    valueChanged = pyqtSignal(int)  # Define a custom signal

    def __init__(self):
        super().__init__()
        self._value = 0

    def increment(self):
        self._value += 1
        self.valueChanged.emit(self._value)  # Emit the signal


def handle_value(value):
    print(f"Counter value: {value}")


counter = Counter()
counter.valueChanged.connect(handle_value)
counter.increment()  # Output: Counter value: 1