import sys
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListView, QLineEdit, QFileDialog
)

# --- Model ---
class TodoModel(QAbstractListModel):
    def __init__(self, todos=None):
        super().__init__()
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole and index.isValid():
            return self.todos[index.row()]
        return None

    def rowCount(self, parent=QModelIndex()):
        # For flat lists, return 0 if parent is valid
        if parent.isValid():
            return 0
        return len(self.todos)

    def addTodo(self, todo):
        self.beginInsertRows(
            QModelIndex(), self.rowCount(), self.rowCount()
        )
        self.todos.append(todo)
        self.endInsertRows()

    def removeTodo(self, row):
        if 0 <= row < self.rowCount():
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.todos[row]
            self.endRemoveRows()

    def setTodos(self, todos):
        # Reset model data entirely
        self.beginResetModel()
        self.todos = todos
        self.endResetModel()


# --- View + Controller ---
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List with Load/Save")

        # Model
        self.model = TodoModel(["Buy milk", "Write code"])

        # View Components
        self.list_view = QListView()
        self.list_view.setModel(self.model)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Add a new task...")

        # Buttons
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_task)

        self.load_button = QPushButton("Load Tasks")
        self.load_button.clicked.connect(self.load_tasks)

        self.save_button = QPushButton("Save Tasks")
        self.save_button.clicked.connect(self.save_tasks)

        # Layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)  # Load/Save buttons at top
        main_layout.addWidget(self.list_view)
        main_layout.addWidget(self.input)
        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.delete_button)
        self.setLayout(main_layout)

    # --- Controller Logic ---
    def add_task(self):
        text = self.input.text()
        if text:
            self.model.addTodo(text)
            self.input.clear()

    def delete_task(self):
        selected = self.list_view.selectionModel().selectedIndexes()
        if selected:
            row = selected[0].row()
            self.model.removeTodo(row)

    def load_tasks(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open Task File", "", "Text Files (*.txt)"
        )
        if filepath:
            with open(filepath, "r") as f:
                tasks = [line.strip() for line in f if line.strip()]
            self.model.setTodos(tasks)

    def save_tasks(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Task File", "", "Text Files (*.txt)"
        )
        if filepath:
            with open(filepath, "w") as f:
                for task in self.model.todos:
                    f.write(f"{task}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())