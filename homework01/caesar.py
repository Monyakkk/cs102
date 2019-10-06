def encrypt_caesar(plaintext: str) -> str:
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for chars in plaintext:
        x = ord(chars)
        if 65 <= x <= 90:
            ciphertext += chr(((x - 62) % 26) + 65)
        elif 97 <= x <= 122:
            ciphertext += chr((x - 94) % 26 + 97)
        else:
            ciphertext += chars
    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for chars in ciphertext:
        x = ord(chars)
        if 65 <= x <= 90:
            plaintext += chr(((x - 68) % 26) + 65)
        elif 97 <= x <= 122:
            plaintext += chr((x - 100) % 26 + 97)
        else:
            plaintext += chars
    return plaintext
