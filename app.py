import os
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from securevault.gui.registration_window import RegistrationWindow
from securevault.gui.login_window import LoginWindow

CONFIG_DIR = Path.home() / ".securevault"
VAULT_DIR = CONFIG_DIR / "vault"
META_FILE = CONFIG_DIR / "meta.dat"

def ensure_dirs():
    CONFIG_DIR.mkdir(exist_ok=True)
    VAULT_DIR.mkdir(exist_ok=True)

def main():
    app = QApplication(sys.argv)
    if not META_FILE.exists():
        ensure_dirs()
        reg = RegistrationWindow(CONFIG_DIR, VAULT_DIR, META_FILE)
        reg.show()
        sys.exit(app.exec())
    else:
        ensure_dirs()
        login = LoginWindow(CONFIG_DIR, VAULT_DIR, META_FILE)
        login.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()