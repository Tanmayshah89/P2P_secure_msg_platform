# secure.py

# DES-like encryption and decryption (simplified XOR-based block cipher)

def pad_text(text):
    """
    Pads the input text to make its length a multiple of 8 (DES block size).
    """
    pad_len = 8 - (len(text) % 8)
    return text + chr(pad_len) * pad_len

def unpad_text(text):
    """
    Removes padding from the text.
    """
    pad_len = ord(text[-1])
    return text[:-pad_len]

def xor_block(block, key_block):
    """
    XORs a block of text with a block of key.
    """
    return ''.join(chr(ord(b) ^ ord(k)) for b, k in zip(block, key_block))

def des_encrypt(plaintext, key):
    """
    Encrypts plaintext using simplified DES-like method with XOR and padding.
    """
    plaintext = pad_text(plaintext)
    ciphertext = ''
    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i+8]
        key_block = (key * 8)[:8]  # Repeat key to 8 bytes if needed
        ciphertext += xor_block(block, key_block)
    return ciphertext

def des_decrypt(ciphertext, key):
    """
    Decrypts ciphertext using simplified DES-like method with XOR and unpadding.
    """
    decrypted = ''
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        key_block = (key * 8)[:8]
        decrypted += xor_block(block, key_block)
    return unpad_text(decrypted)
