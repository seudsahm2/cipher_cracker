# Helpers.py (Create this new file in your caesar app)
def encrypt(plaintext, key):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                ciphertext += chr((ord(char) + key - 65) % 26 + 65)
            else:
                ciphertext += chr((ord(char) + key - 97) % 26 + 97)
        else:
            ciphertext += char
    return ciphertext

def decrypt(ciphertext, key):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                plaintext += chr((ord(char) - key - 65) % 26 + 65)
            else:
                plaintext += chr((ord(char) - key - 97) % 26 + 97)
        else:
            plaintext += char
    return plaintext