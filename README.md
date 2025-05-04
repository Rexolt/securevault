# SecureVault

SecureVault is a modern, dark-themed password manager written in Python and PySide6. It stores each entry as an individually encrypted file with a randomized name and extension, making it harder for malware to locate your data. Built-in process scanning, masked password display, timed reveals and clipboard auto-clearing help keep your secrets safe.

![Logo](image.png "Logo")

## Features

- **Register & Login**  
  First-run registration (username + master password), then secure login with background process scan and visual green/red frame.
- **Encrypted Storage**  
  AES-GCM encryption with keys derived via PBKDF2-HMAC-SHA256; per-file random nonce, randomized file names and extensions.
- **Secure File Layout**  
  Configuration and metadata in `~/.securevault/`, vault files in `~/.securevault/vault/`.
- **Masked Passwords**  
  Table always shows “••••••••” by default; **Show Passwords** reveals them for 5 seconds.
- **Clipboard Copy**  
  **Copy Password** warns you, copies to clipboard, then automatically clears it after 10 seconds.
- **Import / Export**  
  JSON import/export of all entries.
- **Change Master Password**  
  Re-encrypts every entry in place with the new master password.
- **Logout / Exit**  
  Log out to the login screen without quitting, or exit the app entirely.
- **Process Scanner**  
  Scan for suspicious processes (e.g. debuggers) before unlocking your vault.
- **Modern UI**  
  Dark theme, rounded controls, menu bar, toolbar, status bar, responsive dialogs.

---

## Installation

1. Clone or download this repository:
    ```bash
    git clone https://github.com/yourusername/securevault.git
    cd securevault
    ```
2. Install dependencies:
            ```bash
            pip install -r requirements.txt
            ```

3. Run the application:
        ```bash
        python -m securevault.app
        ```

# Usage


## 1. First Run / Registration
You’ll be prompted to choose a username and master password. This creates ```~/.securevault/username.txt```, ```meta.dat```, and ```vault/```.

## 2. Login
***Enter your master password. If no suspicious processes are found, a green frame appears; otherwise, red with warning.***

## 3. Main Window

- Add/Edit/Delete entries via toolbar or menu.

- Show Passwords (5 s) or Copy Password (auto-clear after 10 s) with security warnings.

- Import/Export your vault to/from JSON.

- Change Master Password to rotate encryption keys.

- Logout or Exit from the File menu.

## 4. Data Storage
```bash
~/.securevault/
├── username.txt        # your registered username
├── meta.dat            # 16 B salt + 32 B HMAC tag
└── vault/
    ├── a1b2c3d4e5.f6g7 # encrypted entry blobs
    └── ...

```

# Project Structure

```bash
securevault/
├── app.py                     # application entry point
├── filenames.py               # random file name generator
├── encryption.py              # key derivation & AES-GCM functions
├── storage.py                 # high-level load/save/delete API
├── processes.py               # suspicious process scanner
├── requirements.txt
├── README.md
└── gui/
    ├── entry_dialog.py        # Add/Edit dialog
    ├── login_window.py        # login dialog
    ├── registration_window.py # first-run registration dialog
    ├── change_master_dialog.py
    ├── main_window.py         # QMainWindow with toolbar/menu/status
    ├── style.py               # QSS loader
    └── style.qss              # dark theme styles

```

## Contributing
Contributions, issues and feature requests are welcome! Please open an issue first to discuss your ideas. Pull requests should target the ```main``` branch and include appropriate tests or manual verification steps.

## License
This project is licensed under the **GNU GENERAL PUBLIC LICENSE** License.