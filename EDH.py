#code used for various key derivation algorithms

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
#EDH chosen as keys are ephemeral (generated, used once, discarded) as opposed to (static) DH
#Ephemeral keys allows for forward secrecy

#generates parameters g (modulus) and p (prime)
def generate_parameters():
    parameters = dh.generate_parameters(generator=2, key_size=512) 
    #512 chosen to make code easier to test - (takes less time to establish a sahred key)
    #I am aware that 512 is export grade and would not use it in an actual production enviroment
    return parameters

#generates private/public keys used for EDH
#used for both client/server
def generate_key_pair(parameters):

    private_key = parameters.generate_private_key() #Very large number

    public_key = private_key.public_key() # g^(private_key) mod (p)

    return private_key, public_key


def establish_shared_key(private_key,peer_public_key):

    shared_key = private_key.exchange(peer_public_key) 
    #works via:
    #peer_public_key ^ private_key
    # = (g^(peer_priavte_key) mod p) ^ private_key
    # = (g^(peer_private_key * private_key) mod p)
    # as peer_private_key * private_key == private_key * peer_private_key (symmetric) the same shared key is derived for client/server
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key) #turns the number in shared_key into a standared length 32 byte hash via SHA
    #

    return derived_key

#tests
parameters = generate_parameters()

server_private_key, server_public_key = generate_key_pair(parameters)
client_private_key, client_public_key = generate_key_pair(parameters)

server_derived_key = establish_shared_key(server_private_key,client_public_key)
client_derived_key = establish_shared_key(client_private_key,server_public_key)

print(server_derived_key)
print(client_derived_key)
print(server_derived_key == client_derived_key)

#https://cryptography.io/en/latest/hazmat/primitives/asymmetric/dh/ -used this for help with cryptography library for EDH
