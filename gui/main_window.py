from pathlib import Path
import os, json, gc

from PySide6.QtWidgets import (
    QMainWindow, QApplication, QTableWidget, QTableWidgetItem,
    QToolBar, QStatusBar, QFileDialog, QMessageBox, QDialog
)
from PySide6.QtGui     import QAction, QClipboard
from PySide6.QtCore    import Qt, QTimer

from securevault.storage    import Storage
from securevault.processes  import check_processes
from securevault.encryption import derive_key, verify_master, encrypt_entry
from cryptography.hazmat.primitives import hmac as crypto_hmac, hashes
from cryptography.hazmat.backends import default_backend

from .entry_dialog           import EntryDialog
from .change_master_dialog   import ChangeMasterDialog
from .style                  import style_sheet

class MainWindow(QMainWindow):
    def __init__(self, key: bytes, config_dir: Path, vault_dir: Path, meta_file: Path):
        super().__init__()
        self.key = key
        self.config_dir = config_dir
        self.vault_dir = vault_dir
        self.meta_file = meta_file
        self.storage = Storage(vault_dir)

        self.setWindowTitle("SecureVault")
        self.resize(800, 500)
        self.setStyleSheet(style_sheet)

        
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Name", "Username", "Password", "Category", "Note"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.setCentralWidget(self.table)

        
        toolbar = QToolBar("Main toolbar", self)
        self.addToolBar(toolbar)

        for text, slot, checkable in [
            ("Add",               self.add_entry,        False),
            ("Edit",              self.edit_entry,       False),
            ("Delete",            self.delete_entry,     False),
            ("Copy Password",     self.copy_password,    False),
            ("Show Passwords",    self.show_passwords,   False),
        ]:
            act = QAction(text, self)
            act.triggered.connect(slot)
            act.setCheckable(False)
            toolbar.addAction(act)
        toolbar.addSeparator()

        
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Import…", self.import_json)
        file_menu.addAction("Export…", self.export_json)
        file_menu.addSeparator()
        file_menu.addAction("Change Master Password…", self.change_master)
        file_menu.addSeparator()
        file_menu.addAction("Logout", self.logout)
        file_menu.addAction("Exit", QApplication.instance().quit)

        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Process Scan", self.manual_process_scan)

        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.about_dialog)

       
        self.status = QStatusBar()
        self.setStatusBar(self.status)

       
        self.load_entries()

    def load_entries(self):
       
        self.table.setRowCount(0)
        for fname in self.storage.list_files():
            entry = self.storage.load(self.key, fname)
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(entry["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(entry["user"]))
          
            self.table.setItem(row, 2, QTableWidgetItem("••••••••"))
            self.table.setItem(row, 3, QTableWidgetItem(entry["cat"]))
            self.table.setItem(row, 4, QTableWidgetItem(entry["note"]))
        self.table.resizeColumnsToContents()
        self.status.showMessage(f"{self.table.rowCount()} entries loaded", 3000)

    def add_entry(self):
        dlg = EntryDialog(self)
        if dlg.exec() == QDialog.Accepted:
            data = dlg.get_data()
            self.storage.save(self.key, data)
            self.load_entries()
            self.status.showMessage("Entry added", 2000)

    def edit_entry(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Edit", "Select a row first.")
            return
        fname = self.storage.list_files()[row]
        entry = self.storage.load(self.key, fname)

        dlg = EntryDialog(self, entry)
        if dlg.exec() == QDialog.Accepted:
            new_data = dlg.get_data()
            self.storage.delete(fname)
            self.storage.save(self.key, new_data)
            self.load_entries()
            self.status.showMessage("Entry updated", 2000)

    def delete_entry(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Delete", "Select a row first.")
            return
        if QMessageBox.question(
            self, "Delete",
            "Are you sure you want to delete this entry?",
            QMessageBox.Yes | QMessageBox.No
        ) != QMessageBox.Yes:
            return
        fname = self.storage.list_files()[row]
        self.storage.delete(fname)
        self.load_entries()
        self.status.showMessage("Entry deleted", 2000)

    def copy_password(self):
        
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Copy Password", "Select a row first.")
            return

        fname = self.storage.list_files()[row]
        pwd = self.storage.load(self.key, fname)["pwd"]

       
        if QMessageBox.warning(
            self, "Warning",
            "The password will be placed in the clipboard\n"
            "and will be visible in memory. Continue?",
            QMessageBox.Yes | QMessageBox.No
        ) != QMessageBox.Yes:
            del pwd; gc.collect()
            return

        
        clipboard: QClipboard = QApplication.clipboard()
        clipboard.setText(pwd)
        del pwd; gc.collect()
        
        QTimer.singleShot(10_000, lambda: QApplication.clipboard().clear())

        self.status.showMessage("Password copied to clipboard (will clear in 10s)", 3000)

    def show_passwords(self):
        
        
        for r in range(self.table.rowCount()):
            fname = self.storage.list_files()[r]
            pwd = self.storage.load(self.key, fname)["pwd"]
            
            self.table.item(r, 2).setText(pwd)
            del pwd  
        gc.collect()

        
        QTimer.singleShot(5_000, self.mask_passwords)
        self.status.showMessage("Passwords visible for 5 seconds", 3000)

    def mask_passwords(self):
        """Visszamaskírozza a jelszómezőket."""
        for r in range(self.table.rowCount()):
            self.table.item(r, 2).setText("••••••••")

    def manual_process_scan(self):
        suspicious = check_processes()
        if not suspicious:
            QMessageBox.information(self, "Process Scan", "No suspicious processes found.")
        else:
            names = "\n".join(p["name"] for p in suspicious)
            QMessageBox.warning(self, "Process Scan",
                                f"Suspicious processes detected:\n{names}")

    def import_json(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import JSON", filter="JSON Files (*.json)")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                entries = json.load(f)
            count = 0
            for entry in entries:
                self.storage.save(self.key, entry)
                count += 1
            self.load_entries()
            self.status.showMessage(f"Imported {count} entries", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Import Error", str(e))

    def export_json(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export JSON", filter="JSON Files (*.json)")
        if not path:
            return
        try:
            entries = [
                self.storage.load(self.key, fname)
                for fname in self.storage.list_files()
            ]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(entries, f, ensure_ascii=False, indent=2)
            self.status.showMessage(f"Exported {len(entries)} entries", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))

    def change_master(self):
        dlg = ChangeMasterDialog(self)
        if dlg.exec() != QDialog.Accepted:
            return
        curr_pw, new_pw = dlg.get_passwords()
        try:
            old_key = verify_master(curr_pw, str(self.meta_file))
        except Exception:
            QMessageBox.critical(self, "Error", "Current master password is incorrect.")
            return
        salt = os.urandom(16)
        new_key = derive_key(new_pw, salt)
        h = crypto_hmac.HMAC(new_key, hashes.SHA256(), backend=default_backend())
        h.update(b"master-check")
        tag = h.finalize()
        with open(self.meta_file, "wb") as f:
            f.write(salt + tag)
        for fname in self.storage.list_files():
            entry = self.storage.load(old_key, fname)
            blob = encrypt_entry(new_key, entry)
            with open(self.vault_dir / fname, "wb") as f:
                f.write(blob)
        self.key = new_key
        QMessageBox.information(self, "Success", "Master password changed successfully.")

    def logout(self):
        from .login_window import LoginWindow
        self.close()
        login = LoginWindow(self.config_dir, self.vault_dir, self.meta_file)
        login.show()

    def about_dialog(self):
        QMessageBox.information(
            self, "About SecureVault",
            "SecureVault v1.0\nA modern, password manager. By: Rexolt"
        )
