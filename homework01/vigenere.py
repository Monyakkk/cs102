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
        if "A" <= keyword[i % len(keyword)] <= "Z":
            y -= ord("A")
        if "a" <= keyword[i % len(keyword)] <= "z":
            y -= ord("a")
        if "A" <= plaintext[i] <= "Z":
            ciphertext += chr(((x - ord("A") + y) % 26) + ord("A"))
        elif "a" <= plaintext[i] <= "z":
            ciphertext += chr((x - ord("a") + y) % 26 + ord("a"))
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
    for i in range (len(ciphertext)):
        x = ord(ciphertext[i])
        y = ord(keyword[i % len(keyword)])
        if "A" <= keyword[i % len(keyword)] <= "Z":
            y -= ord("A")
        if "a" <= keyword[i % len(keyword)] <= "z":
            y -= ord("a")
        if "A" <= ciphertext[i] <= "Z":
            plaintext += chr(((x - ord("A") - y) % 26) + ord("A"))
        elif "a" <= ciphertext[i] <= "z":
            plaintext += chr((x - ord("a") - y) % 26 + ord("a"))
        else:
            plaintext += chr(x)
    return plaintext





