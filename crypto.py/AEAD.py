import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
#chose Poly1350 specifically as it is authenticated

def encrypt(plaintext,key,authenticate):

    nonce = os.urandom(12) #produces 12 bytes of random data for a nonce

    chacha = ChaCha20Poly1305(key) #takes an exactly 32 byte key 

    ciphertext = chacha.encrypt(nonce, plaintext, authenticate) #chacha is a stream cipher thus plaintext can be any length - no need for modes of operation

    return ciphertext, nonce

def decrypt(ciphertext,key,nonce,authenticate):

    chacha = ChaCha20Poly1305(key) #takes an exactly 32 byte key

    plaintext = chacha.decrypt(nonce, ciphertext, authenticate)

    return plaintext

#quick test
secret = b"my seeecrets"
authenticate = b"my identity"
key = ChaCha20Poly1305.generate_key()
ciphertext, nonce = encrypt(secret,key,authenticate)

print(ciphertext)

plaintext = decrypt(ciphertext,key,nonce,authenticate)

if plaintext == secret:
    print(True)

#used https://cryptography.io/en/latest/hazmat/primitives/aead/ when I was first implemting the encrypt and decrypt functions
#used https://www.cryptography-primer.info/algorithms/chacha/ for a more in depth understanding of chacha


