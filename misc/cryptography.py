"""
Tool to encrypt a password
"""

from cryptography.fernet import Fernet

# Generate key
KEY = Fernet.generate_key()
print('Your key: ' + '\033[92m' + str(KEY) + '\033[0m')

prompt = 'Type your password: '

pw = input(prompt)
byte_pw = pw.encode('utf-8')

cipher_suite = Fernet(KEY)
ciphered_pw = cipher_suite.encrypt(byte_pw)

# Store password in encrypted bin file
with open('password.bin', 'wb') as file_object:
    file_object.write(ciphered_pw)

# Decrypt password
with open('password.bin', 'rb') as f:
    for line in f:
        encrypted_pw = line

cipher_suite = Fernet(KEY)
password = bytes(cipher_suite.decrypt(encrypted_pw)).decode('utf-8')

print('\033[36m' + f"Your password '{password}' was successfully encrypted!")
