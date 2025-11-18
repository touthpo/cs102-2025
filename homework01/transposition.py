def decrypt_transposition(ciphertext, block_size, id1, id2):
    if id1 >= block_size or id2 >= block_size:
        raise ValueError
    if id1 < 0 or id2 < 0:
        raise ValueError
    text = ciphertext.replace(" ", "").upper()
    remainder = len(text) % block_size
    if remainder != 0:
        text += "X" * (block_size - remainder)
    decrypted_text = ""
    for i in range(0, len(text), block_size):
        block = text[i:i + block_size]
        block_chars = list(block)
        block_chars[id1], block_chars[id2] = block_chars[id2], block_chars[id1]
        decrypted_text += "".join(block_chars)
    return decrypted_text

    
     
        
    
