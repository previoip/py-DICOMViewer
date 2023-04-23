from hashlib import sha1

def sha1_digest(msg: bytes):
    sha1_c = sha1()
    sha1_c.update(msg)
    return sha1_c.digest()

def sha1_to_hex(msg: bytes):
    return sha1_digest(msg).hex()