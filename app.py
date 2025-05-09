import os
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from securevault.gui.registration_window import RegistrationWindow
from securevault.gui.recovery_dialog     import RecoveryKeysDialog
from securevault.gui.login_window        import LoginWindow

CONFIG_DIR = Path.home() / ".securevault"
VAULT_DIR  = CONFIG_DIR / "vault"
META_FILE  = CONFIG_DIR / "meta.dat"

def ensure_dirs():
    CONFIG_DIR.mkdir(exist_ok=True)
    VAULT_DIR.mkdir(exist_ok=True)

def main():
    app = QApplication(sys.argv)
    ensure_dirs()

   
    if not META_FILE.exists():
        reg = RegistrationWindow(CONFIG_DIR, VAULT_DIR, META_FILE)
        
        if hasattr(reg, "exec"):
            reg.exec()
        else:
            reg.show()
            app.exec()
       
        rec = RecoveryKeysDialog(CONFIG_DIR)
        rec.exec()

    
    login = LoginWindow(CONFIG_DIR, VAULT_DIR, META_FILE)
    login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()