import socket
import json
import random


# Do not change this function
def connect_and_get_socket():
    port = 4321
    host = 'localhost'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


# Do not change this function
def send(p, q, g, gx, client_socket):
    encoded_data = json.dumps({'p': p, 'q': q, 'g': g, 'gx': gx})
    client_socket.send(encoded_data.encode('ascii'))


# Do not change this function
def receive(client_socket):
    # Receive no more than 1024 bytes
    data = client_socket.recv(1024)
    return json.loads(data)


def generate_x(q):
    # Changed this to generate a random private key x in the range [1, q-1]
    return random.randint(1, q - 1)


def compute_g_x_mod_p(g, x, p):
    # Computes Alice's public key gx = g^x mod p using pow(base,exponent,modulo). Makes it more efficent
    return pow(g, x, p)


def compute_shared_secret(gy, x, p):
    # Computes the shared secret: (gy)^x mod p
    return pow(gy, x, p)


def exchange_shared_secret():
    # Some public parameters. Both q and 2q+1 are primes.
    q = 51733955177920554523556498583707150890400087957938764433568354798808049950581
    p = 2 * q + 1
    g = 2

    # Generate x and compute gx:
    x = generate_x(q)
    # Changed the parameters to compute her public key gx
    gx = compute_g_x_mod_p(g, x, p)

    # Connect to Bob and run DH
    s = connect_and_get_socket()
    # Send public parameters as well as gx to
    send(p, q, g, gx, s)
    # Receive gy
    data = receive(s)
    gy = data['gy']

    # Compute shared secret
    # Changed the parameters with the correct ones to compute the shared secret (gy^x mod p) using Bob"s public key and Alice"s private key.
    shared_secret = compute_shared_secret(gy, x, p)
    print(f"Alice's computed shared secret: {shared_secret}")


if __name__ == "__main__":
    exchange_shared_secret()

