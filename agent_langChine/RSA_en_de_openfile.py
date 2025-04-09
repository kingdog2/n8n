from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# 讀取Key
def open_private_key():
    with open(r'C:\Users\f2201\Downloads\private_key.pem', 'rb') as private_file:
        key = RSA.import_key(private_file.read())
    return key

def open_public_key():
    with open(r'C:\Users\f2201\Downloads\public_key.pem', 'rb') as public_file:
        key = RSA.import_key(public_file.read())
    return key

# 加密
def encrypt_message(public_key, message):
    cipher = PKCS1_OAEP.new(public_key)  # 使用 PKCS1_OAEP 填充方式
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

# 解密
def decrypt_message(private_key, encrypted_message):
    cipher = PKCS1_OAEP.new(private_key)  # 使用 PKCS1_OAEP 填充方式
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message.decode()

public_key = open_public_key()
private_key = open_private_key()

message = "f20653ede959a30dd3abe20f53d37cb7767b541b0957de3ae3c7c2daeb513586"
encrypted_message = encrypt_message(public_key, message)
print("Encrypted:", encrypted_message)
with open(r'C:\Users\f2201\Downloads\encrypted_message.txt', 'wb') as file:
    file.write(encrypted_message)
    
with open(r'C:\Users\f2201\Downloads\encrypted_message.txt', 'rb') as file:
    a = file.read()
decrypted_message = decrypt_message(private_key, a)
print("Decrypted:", decrypted_message)
