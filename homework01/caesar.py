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
        if "A" <= chars <= "Z":
            ciphertext += chr(((x - ord("A") + 3) % 26) + ord("A"))
        elif "a" <= chars <= "z":
            ciphertext += chr((x - ord("a") + 3) % 26 + ord("a"))
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
        if "A" <= chars <= "Z":
            plaintext += chr(((x - ord('A') - 3) % 26) + ord('A'))
        elif "a" <= chars <= "z":
            plaintext += chr((x - ord('a') - 3) % 26 + ord('a'))
        else:
            plaintext += chars
    return plaintext
