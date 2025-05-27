import sys
import random
import string
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QSlider, QPushButton, QCheckBox,
                             QLineEdit, QGroupBox, QSpinBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QClipboard

class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Generator")
        self.setMinimumSize(500, 400)
        self.resize(600, 500)

        # Initialize variables
        self.current_password = ""

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create UI components
        self.create_length_section(main_layout)
        self.create_options_section(main_layout)
        self.create_validation_section(main_layout)
        self.create_password_display_section(main_layout)
        self.create_action_buttons(main_layout)

        # Generate initial password
        self.generate_password()

    def create_length_section(self, parent_layout):
        """Create password length selection section"""
        length_group = QGroupBox("Password Length")
        length_layout = QVBoxLayout(length_group)

        # Length display and controls
        length_control_layout = QHBoxLayout()

        # Decrement button
        self.decrement_btn = QPushButton("-")
        self.decrement_btn.setFixedSize(30, 30)
        self.decrement_btn.clicked.connect(self.decrement_length)

        # Length display
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(8, 64)
        self.length_spinbox.setValue(12)
        self.length_spinbox.valueChanged.connect(self.update_slider)

        # Increment button
        self.increment_btn = QPushButton("+")
        self.increment_btn.setFixedSize(30, 30)
        self.increment_btn.clicked.connect(self.increment_length)

        length_control_layout.addWidget(self.decrement_btn)
        length_control_layout.addWidget(self.length_spinbox)
        length_control_layout.addWidget(self.increment_btn)
        length_control_layout.addStretch()

        # Slider
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setRange(8, 64)
        self.length_slider.setValue(12)
        self.length_slider.valueChanged.connect(self.update_spinbox)

        length_layout.addLayout(length_control_layout)
        length_layout.addWidget(self.length_slider)

        parent_layout.addWidget(length_group)

    def create_options_section(self, parent_layout):
        """Create character type options section"""
        options_group = QGroupBox("Character Types")
        options_layout = QVBoxLayout(options_group)

        # Checkboxes for character types
        self.lowercase_cb = QCheckBox("Lowercase letters (a-z)")
        self.lowercase_cb.setChecked(True)
        self.lowercase_cb.stateChanged.connect(self.validate_selections)

        self.uppercase_cb = QCheckBox("Uppercase letters (A-Z)")
        self.uppercase_cb.setChecked(True)
        self.uppercase_cb.stateChanged.connect(self.validate_selections)

        self.digits_cb = QCheckBox("Digits (0-9)")
        self.digits_cb.setChecked(True)
        self.digits_cb.stateChanged.connect(self.validate_selections)

        self.symbols_cb = QCheckBox("Symbols (!@#$%^&*)")
        self.symbols_cb.setChecked(False)
        self.symbols_cb.stateChanged.connect(self.validate_selections)

        options_layout.addWidget(self.lowercase_cb)
        options_layout.addWidget(self.uppercase_cb)
        options_layout.addWidget(self.digits_cb)
        options_layout.addWidget(self.symbols_cb)

        parent_layout.addWidget(options_group)

    def create_validation_section(self, parent_layout):
        """Create validation option section"""
        validation_group = QGroupBox("Validation Options")
        validation_layout = QVBoxLayout(validation_group)

        self.validate_cb = QCheckBox("Ensure password contains at least one character from each selected type")
        self.validate_cb.setChecked(True)

        validation_layout.addWidget(self.validate_cb)
        parent_layout.addWidget(validation_group)

    def create_password_display_section(self, parent_layout):
        """Create password display section"""
        display_group = QGroupBox("Generated Password")
        display_layout = QVBoxLayout(display_group)

        # Password display
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setFont(QFont("Courier", 12))
        self.password_display.setMinimumHeight(40)

        # Show/Hide toggle
        show_layout = QHBoxLayout()
        self.show_password_cb = QCheckBox("Show password")
        self.show_password_cb.setChecked(True)
        self.show_password_cb.stateChanged.connect(self.toggle_password_visibility)

        show_layout.addWidget(self.show_password_cb)
        show_layout.addStretch()

        display_layout.addWidget(self.password_display)
        display_layout.addLayout(show_layout)

        parent_layout.addWidget(display_group)

    def create_action_buttons(self, parent_layout):
        """Create action buttons section"""
        button_layout = QHBoxLayout()

        # Generate button
        self.generate_btn = QPushButton("Generate Password")
        self.generate_btn.setMinimumHeight(40)
        self.generate_btn.clicked.connect(self.generate_password)

        # Copy button
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.setMinimumHeight(40)
        self.copy_btn.clicked.connect(self.copy_password)

        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.copy_btn)

        parent_layout.addLayout(button_layout)

    def increment_length(self):
        """Increment password length"""
        current_value = self.length_spinbox.value()
        if current_value < 64:
            self.length_spinbox.setValue(current_value + 1)

    def decrement_length(self):
        """Decrement password length"""
        current_value = self.length_spinbox.value()
        if current_value > 8:
            self.length_spinbox.setValue(current_value - 1)

    def update_slider(self, value):
        """Update slider when spinbox changes"""
        self.length_slider.setValue(value)

    def update_spinbox(self, value):
        """Update spinbox when slider changes"""
        self.length_spinbox.setValue(value)

    def validate_selections(self):
        """Ensure at least one character type is selected"""
        any_selected = (self.lowercase_cb.isChecked() or
                        self.uppercase_cb.isChecked() or
                        self.digits_cb.isChecked() or
                        self.symbols_cb.isChecked())

        if not any_selected:
            # Re-check the previously unchecked box
            sender = self.sender()
            sender.setChecked(True)
            QMessageBox.warning(self, "Warning",
                                "At least one character type must be selected!")

    def generate_password(self):
        """Generate a new password based on selected options"""
        length = self.length_spinbox.value()

        # Build character set based on selections
        charset = ""
        required_chars = []

        if self.lowercase_cb.isChecked():
            charset += string.ascii_lowercase
            if self.validate_cb.isChecked():
                required_chars.append(random.choice(string.ascii_lowercase))

        if self.uppercase_cb.isChecked():
            charset += string.ascii_uppercase
            if self.validate_cb.isChecked():
                required_chars.append(random.choice(string.ascii_uppercase))

        if self.digits_cb.isChecked():
            charset += string.digits
            if self.validate_cb.isChecked():
                required_chars.append(random.choice(string.digits))

        if self.symbols_cb.isChecked():
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            charset += symbols
            if self.validate_cb.isChecked():
                required_chars.append(random.choice(symbols))

        # Generate password
        if self.validate_cb.isChecked() and required_chars:
            # Start with required characters
            password_chars = required_chars[:]
            # Fill remaining length with random characters
            remaining_length = length - len(required_chars)
            password_chars.extend(random.choices(charset, k=remaining_length))
            # Shuffle to avoid predictable patterns
            random.shuffle(password_chars)
            self.current_password = ''.join(password_chars)
        else:
            # Generate completely random password
            self.current_password = ''.join(random.choices(charset, k=length))

        # Update display
        self.update_password_display()

    def update_password_display(self):
        """Update the password display based on show/hide setting"""
        if self.show_password_cb.isChecked():
            self.password_display.setText(self.current_password)
        else:
            self.password_display.setText('*' * len(self.current_password))

    def toggle_password_visibility(self):
        """Toggle between showing and hiding the password"""
        self.update_password_display()

    def copy_password(self):
        """Copy the current password to clipboard"""
        if self.current_password:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.current_password)
            QMessageBox.information(self, "Success",
                                    "Password copied to clipboard!")
        else:
            QMessageBox.warning(self, "Warning",
                                "No password to copy!")