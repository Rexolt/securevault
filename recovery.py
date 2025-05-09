# securevault/recovery.py

import os, json, base64, secrets, string, datetime
from pathlib import Path
from cryptography.hazmat.primitives import hmac, hashes
from cryptography.hazmat.backends import default_backend

RECOVERY_FILE = "recovery.json"
LOG_FILE      = "recovery.log"

def _load_data(config_dir: Path) -> dict:
    p = config_dir / RECOVERY_FILE
    if not p.exists():
        raise FileNotFoundError("No recovery file")
    return json.loads(p.read_text(encoding="utf-8"))

def _save_data(config_dir: Path, data: dict):
    p = config_dir / RECOVERY_FILE
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")

def log_recovery_attempt(config_dir: Path, key: str, success: bool):
    p = config_dir / LOG_FILE
    now = datetime.datetime.utcnow().isoformat()
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"{now} | key={key} | success={success}\n")

def generate_recovery_keys(config_dir: Path, num: int = 10) -> list[str]:
    salt = os.urandom(16)
    salt_b64 = base64.b64encode(salt).decode()
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + "-"
    plain_keys = []
    entries = []
    for _ in range(num):
        length = secrets.choice(range(4, 8))
        k = "".join(secrets.choice(alphabet) for __ in range(length))
        h = hmac.HMAC(salt, hashes.SHA256(), backend=default_backend())
        h.update(k.encode("utf-8"))
        digest = h.finalize()
        entries.append({
            "hash": base64.b64encode(digest).decode(),
            "used": False,
            "created": datetime.datetime.utcnow().isoformat()
        })
        plain_keys.append(k)
    data = {"salt": salt_b64, "entries": entries}
    _save_data(config_dir, data)
    return plain_keys

def verify_and_consume(config_dir: Path, key: str) -> bool:
    data = _load_data(config_dir)
    salt = base64.b64decode(data["salt"])
    success = False
    for rec in data["entries"]:
        if rec.get("used"):
            continue
        h = hmac.HMAC(salt, hashes.SHA256(), backend=default_backend())
        h.update(key.encode("utf-8"))
        if h.finalize() == base64.b64decode(rec["hash"]):
            rec["used"]    = True
            rec["used_at"] = datetime.datetime.utcnow().isoformat()
            success = True
            break
    if success:
        _save_data(config_dir, data)
    log_recovery_attempt(config_dir, key, success)
    return success

def list_recovery_status(config_dir: Path) -> list[dict]:
    data = _load_data(config_dir)
    return [
        {
            "index":   idx,
            "used":    rec.get("used", False),
            "created": rec.get("created"),
            "used_at": rec.get("used_at")
        }
        for idx, rec in enumerate(data["entries"])
    ]
