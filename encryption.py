from Crypto.Cipher import AES
import base64

def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

def adjust_key_length(key):
    key_length = len(key.encode('utf-8'))
    if key_length not in {16, 24, 32}:
        raise ValueError("Incorrect AES key length (must be 16, 24, or 32 bytes)")
    return key

def encrypt_file(file_content, key):
    key = adjust_key_length(key)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    padded_data = pad(file_content)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data)

def decrypt_file(encrypted_file_content, key):
    key = adjust_key_length(key)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    encrypted_data = base64.b64decode(encrypted_file_content)
    decrypted_data = cipher.decrypt(encrypted_data).rstrip(b"\0")
    return decrypted_data
