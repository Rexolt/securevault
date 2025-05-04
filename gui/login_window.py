from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from .style import style_sheet
from securevault.encryption import verify_master
from securevault.processes import check_processes
from .main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self, config_dir: Path, vault_dir: Path, meta_file: Path):
        super().__init__()
        self.config_dir = config_dir
        self.vault_dir = vault_dir
        self.meta_file = meta_file

        self.setWindowTitle("Login - SecureVault")
        self.setStyleSheet(style_sheet)
        self.resize(400, 220)

        lay = QVBoxLayout(self)
        user = open(config_dir / "username.txt", encoding="utf-8").read().strip()
        lay.addWidget(QLabel(f"Username: {user}"))
        self.user_input = QLineEdit(user)
        self.user_input.setReadOnly(True)
        lay.addWidget(self.user_input)

        lay.addWidget(QLabel("Master Password:"))
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.Password)
        lay.addWidget(self.pw_input)

        btn = QPushButton("Login")
        btn.clicked.connect(self.attempt_login)
        lay.addWidget(btn)

    def attempt_login(self):
        pw = self.pw_input.text()
        try:
            key = verify_master(pw, str(self.meta_file))
        except Exception:
            QMessageBox.critical(self, "Error", "Wrong username or master password.")
            return

        suspicious = check_processes()
        if suspicious:
            reply = QMessageBox.warning(
                self, "Warning",
                "Suspicious processes detected:\n" +
                "\n".join(p['name'] for p in suspicious),
                QMessageBox.Ok | QMessageBox.Cancel
            )
            if reply == QMessageBox.Cancel:
                return

      
        self.hide()
        self.main = MainWindow(key, self.config_dir, self.vault_dir, self.meta_file)
        self.main.show()
