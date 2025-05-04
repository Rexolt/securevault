from PySide6.QtWidgets import (
    QDialog, QDialogButtonBox, QFormLayout,
    QLineEdit, QLabel, QMessageBox
)
from PySide6.QtCore import Qt

class EntryDialog(QDialog):
    def __init__(self, parent=None, entry=None):
        super().__init__(parent)
        self.setWindowTitle("Add Entry" if entry is None else "Edit Entry")
        self.setModal(True)
        self.resize(400, 0)

        # Form
        form = QFormLayout(self)
        self.name_edit = QLineEdit(entry["name"] if entry else "")
        self.user_edit = QLineEdit(entry["user"] if entry else "")
        self.pwd_edit  = QLineEdit(entry["pwd"]  if entry else "")
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        self.cat_edit  = QLineEdit(entry["cat"]  if entry else "")
        self.note_edit = QLineEdit(entry["note"] if entry else "")

        form.addRow("Name:",      self.name_edit)
        form.addRow("Username:",  self.user_edit)
        form.addRow("Password:",  self.pwd_edit)
        form.addRow("Category:",  self.cat_edit)
        form.addRow("Note:",      self.note_edit)

        # Buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        self.buttons.accepted.connect(self.validate)
        self.buttons.rejected.connect(self.reject)
        form.addRow(self.buttons)

    def validate(self):
        # Egyszerű validáció: kötelező mezők
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Validation", "Name cannot be empty.")
            return
        if not self.pwd_edit.text():
            QMessageBox.warning(self, "Validation", "Password cannot be empty.")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "name": self.name_edit.text().strip(),
            "user": self.user_edit.text().strip(),
            "pwd":  self.pwd_edit.text(),
            "cat":  self.cat_edit.text().strip(),
            "note": self.note_edit.text().strip()
        }
