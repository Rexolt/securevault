import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def create_master_meta(password: str, meta_path: str):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(b"master-check")
    tag = h.finalize()
    with open(meta_path, "wb") as f:
        f.write(salt + tag)

    password = None

def verify_master(password: str, meta_path: str) -> bytes:
    data = open(meta_path, "rb").read()
    salt, tag = data[:16], data[16:]
    key = derive_key(password, salt)
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(b"master-check")
    h.verify(tag) 
    password = None
    return key

def encrypt_entry(key: bytes, entry: dict) -> bytes:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    plaintext = json_bytes = entry_to_bytes(entry)
    ct = aesgcm.encrypt(nonce, json_bytes, None)
    return nonce + ct

def decrypt_entry(key: bytes, blob: bytes) -> dict:
    aesgcm = AESGCM(key)
    nonce, ct = blob[:12], blob[12:]
    pt = aesgcm.decrypt(nonce, ct, None)
    return bytes_to_entry(pt)

def entry_to_bytes(entry: dict) -> bytes:
    import json
    return json.dumps(entry, ensure_ascii=False).encode()

def bytes_to_entry(b: bytes) -> dict:
    import json
    return json.loads(b.decode())
