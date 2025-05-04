import uuid
import secrets
import string

def random_filename():

    name = uuid.uuid4().hex
    ext_len = secrets.choice([4, 5, 6])
    ext_chars = string.ascii_lowercase + string.digits
    ext = ''.join(secrets.choice(ext_chars) for _ in range(ext_len))
    return f"{name}.{ext}"