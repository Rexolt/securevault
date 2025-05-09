

from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit,
    QDialogButtonBox, QPushButton, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from securevault.recovery import generate_recovery_keys

class RecoveryKeysDialog(QDialog):
    def __init__(self, config_dir: Path, parent=None):
        super().__init__(parent)
        self.config_dir = config_dir
        self.setWindowTitle("Recovery Keys")
        self.resize(400, 300)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(
            "Please save these one-time recovery keys in a secure place.\n"
            "You can use each key once to reset your master password.\n"
            "If you lose them, you cannot recover your vault."
        ))

        
        self.keys = generate_recovery_keys(config_dir)
        self.text = QTextEdit("\n".join(self.keys))
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

      
        btns = QDialogButtonBox()
        self.save_btn = QPushButton("Download as .txt")
        self.save_btn.clicked.connect(self._save_txt)
        btns.addButton(self.save_btn, QDialogButtonBox.ActionRole)

        self.ok_btn = QPushButton("I have saved them")
        self.ok_btn.clicked.connect(self.accept)
        btns.addButton(self.ok_btn, QDialogButtonBox.AcceptRole)

        layout.addWidget(btns)

    def _save_txt(self):
  
        reply = QMessageBox.warning(
            self, "Warning",
            "Saving to a .txt file may expose your keys to other programs.\n"
            "Proceed at your own risk.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save Recovery Keys", filter="Text Files (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.keys))
            QMessageBox.information(self, "Saved", f"Recovery keys saved to:\n{path}")
