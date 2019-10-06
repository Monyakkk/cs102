def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i in range (len(plaintext)):
        x = ord(plaintext[i])
        y = ord(keyword[i % len(keyword)])
        if 65 <= y <= 90:
            y -= 65
        if 97 <= y <= 122:
            y -= 97
        if 65 <= x <= 90:
            ciphertext += chr(((x - 65 + y) % 26) + 65)
        elif 97 <= x <= 122:
            ciphertext += chr((x - 97 + y) % 26 + 97)
        else:
            ciphertext += chr(x)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i in range (len(plaintext)):
        x = ord(plaintext[i])
        y = ord(keyword[i % len(keyword)])
        if 65 <= y <= 90:
            y -= 65
        if 97 <= y <= 122:
            y -= 97
        if 65 <= x <= 90:
            plaintext += chr(((x - 65 - y) % 26) + 65)
        elif 97 <= x <= 122:
            plaintext += chr((x - 97 - y) % 26 + 97)
        else:
            plaintext += chr(x)
    return plaintext





