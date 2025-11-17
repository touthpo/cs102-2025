def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword = keyword.upper()
    key_length = len(keyword)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            key_char = keyword[i % key_length]
            key_shift = ord(key_char) - ord("A")
            
            if char.isupper():
                start = ord("A")
                encrypted_char = chr((ord(char) - start + key_shift) % 26 + start)
                ciphertext += encrypted_char
            else:
                start = ord("a")
                encrypted_char = chr((ord(char) - start + key_shift) % 26 + start)
                ciphertext += encrypted_char
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    
    keyword = keyword.upper()
    key_length = len(keyword)
    
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            key_char = keyword[i % key_length]
            key_shift = ord(key_char) - ord("A")
            
            if char.isupper():
                start = ord("A")
                decrypted_char = chr((ord(char) - start - key_shift) % 26 + start)
                plaintext += decrypted_char
            else:
                start = ord("a")
                decrypted_char = chr((ord(char) - start - key_shift) % 26 + start)
                plaintext += decrypted_char
        else:
            plaintext += char
    return plaintext
