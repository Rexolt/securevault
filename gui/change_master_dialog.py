from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
)
from PySide6.QtCore import Qt

class ChangeMasterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Master Password")
        self.setModal(True)
        self.resize(400, 0)
        layout = QFormLayout(self)

        self.curr_pw = QLineEdit()
        self.curr_pw.setEchoMode(QLineEdit.Password)
        layout.addRow("Current Password:", self.curr_pw)

        self.new_pw = QLineEdit()
        self.new_pw.setEchoMode(QLineEdit.Password)
        layout.addRow("New Password:", self.new_pw)

        self.new_pw2 = QLineEdit()
        self.new_pw2.setEchoMode(QLineEdit.Password)
        layout.addRow("Confirm New Password:", self.new_pw2)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.validate)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def validate(self):
        cpw = self.curr_pw.text()
        npw = self.new_pw.text()
        npw2 = self.new_pw2.text()
        if not cpw or not npw:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return
        if npw != npw2:
            QMessageBox.warning(self, "Error", "New passwords do not match.")
            return
        self.accept()

    def get_passwords(self):
        return self.curr_pw.text(), self.new_pw.text()
