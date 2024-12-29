import socket
import json
import random


# Do not change this function
def wait_and_get_socket():
    port = 4321
    host = 'localhost'
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((host, port))
    serversocket.listen(1)
    (clientsocket, address) = serversocket.accept()
    print(f"Running Diffie-Hellman key exchange protocol with {str(address)}")
    return clientsocket


# Do not change this function
def send(gy, client_socket):
    encoded_data = json.dumps({'gy': gy})
    client_socket.send(encoded_data.encode('ascii'))


# Do not change this function
def receive(client_socket):
    # Receive no more than 1024 bytes
    data = client_socket.recv(1024)
    return json.loads(data)


def generate_y(q):
     # Changed this to generate a random private key y in the range [1, q-1]
    return random.randint(1, q - 1)


def compute_g_y_mod_p(g, y, p):
    # Computes Bob's public key gy = g^y mod p using pow(base,exponent,modulo). Makes it more efficent
    return pow(g, y, p)


def compute_shared_secret(gx, y, p):
   # Computes the shared secret: (gx)^y mod p. 
    return pow(gx, y, p)


def exchange_shared_secret():
    # Establish socket and wait for incoming connections
    s = wait_and_get_socket()

    # Receive public parameters from Alice
    data = receive(s)
    q = data['q']
    p = data['p']
    g = data['g']
    gx = data['gx']

    # Generate y and compute gy:
    y = generate_y(q)
    # Here changed the parameters with the correct ones. Computed Bob's public key gy = g^y mod p
    gy = compute_g_y_mod_p(g, y, p)

    # Compute shared secret
    # Changed the parameters with the correct ones
    shared_secret = compute_shared_secret(gx, y, p)
    print(f"Bob's computed shared secret: {shared_secret}")

    # Here changed the first parameter to gy and it sends gy to Alice. 
    send(gy, s)
    s.close()


if __name__ == "__main__":
    exchange_shared_secret()

