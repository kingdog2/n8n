# pip install pycryptodome
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

# Generate RSA keys
def generate_and_save_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    with open('private_key.pem', 'wb') as private_file:
        private_file.write(private_key)
    with open('public_key.pem', 'wb') as public_file:
        public_file.write(public_key)
    return private_key, public_key

# 加密
def encrypt_message(public_key, message):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

# 解密
def decrypt_message(private_key, encrypted_message):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message.decode()


if __name__ == "__main__":
    try:
        private_key, public_key = generate_and_save_rsa_keys()
        print("Private Key:")
        print(private_key.decode())
        print("Public Key:")
        print(public_key.decode())
        print("="*100)
        
        # 加密
        message = "f20653ede959a30dd3abe20f53d37cb7767b541b0957de3ae3c7c2daeb513586"
        encrypted_message = encrypt_message(public_key, message)
        print("\nEncrypted Message:", encrypted_message)    
        # 解密
        decrypted_message = decrypt_message(private_key, encrypted_message)
        print("\nDecrypted Message:", decrypted_message)
    except Exception as e:
        print(e)