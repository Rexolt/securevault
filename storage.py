import os
from pathlib import Path
from .filenames import random_filename
from .encryption import encrypt_entry, decrypt_entry

class Storage:
    def __init__(self, vault_dir: Path):
        self.vault_dir = vault_dir

    def save(self, key: bytes, entry: dict) -> str:
        blob = encrypt_entry(key, entry)
        fname = random_filename()
        with open(self.vault_dir / fname, "wb") as f:
            f.write(blob)
        return fname

    def list_files(self) -> list[str]:
        return [f for f in os.listdir(self.vault_dir) if os.path.isfile(self.vault_dir / f)]

    def load(self, key: bytes, fname: str) -> dict:
        data = open(self.vault_dir / fname, "rb").read()
        return decrypt_entry(key, data)

    def delete(self, fname: str):
        os.remove(self.vault_dir / fname)
