# Basic DES-style encryption (not real DES, just simulating steps)
def des_encrypt(plaintext):
    return ''.join(chr((ord(char) + 5) % 256) for char in plaintext)

def des_decrypt(ciphertext):
    return ''.join(chr((ord(char) - 5) % 256) for char in ciphertext)

