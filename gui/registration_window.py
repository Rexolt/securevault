import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from .style import style_sheet
from securevault.encryption import create_master_meta
from securevault.storage import Storage

class RegistrationWindow(QWidget):
    def __init__(self, config_dir: Path, vault_dir: Path, meta_file: Path):
        super().__init__()
        self.config_dir = config_dir
        self.vault_dir = vault_dir
        self.meta_file = meta_file

        self.setWindowTitle("Register - SecureVault")
        self.setStyleSheet(style_sheet)
        self.resize(400, 250)

        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Username:"))
        self.user_input = QLineEdit(); lay.addWidget(self.user_input)

        lay.addWidget(QLabel("Master Password:"))
        self.pw_input = QLineEdit(); self.pw_input.setEchoMode(QLineEdit.Password); lay.addWidget(self.pw_input)

        lay.addWidget(QLabel("Confirm Password:"))
        self.pw_confirm = QLineEdit(); self.pw_confirm.setEchoMode(QLineEdit.Password); lay.addWidget(self.pw_confirm)

        btn = QPushButton("Register"); btn.clicked.connect(self.register); lay.addWidget(btn)

    def register(self):
        user = self.user_input.text().strip()
        pw = self.pw_input.text()
        pw2 = self.pw_confirm.text()
        if not user or not pw:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return
        if pw != pw2:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
        # meta és vault mappa már fennáll az app.py miatt
        # elmentjük a felhasználónevet
        with open(self.config_dir / "username.txt", "w", encoding="utf-8") as f:
            f.write(user)
        # létrehozzuk a master meta fájlt
        create_master_meta(pw, str(self.meta_file))
        # üres vault mappa
        Storage(self.vault_dir)  # init only
        QMessageBox.information(self, "Done", "Registration successful. Please login now.")
        self.close()
