import socket
from Util import Util
import random

util = Util()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((util.server_address_builder()))
serv.listen(2)

alice_conn = ''
bob_conn = ''

x_prime = 0
y_prime = 0

while True:
    conn, addr = serv.accept()
    data = str(conn.recv(4096).decode())
    if data.split(':')[0] == 'x_prime':
        alice_conn = conn
        x_prime = int(data.split(':')[1])
        print(x_prime)
    if data.split(':')[0] == 'y_prime':
        bob_conn = conn
        y_prime = int(data.split(':')[1])
        print(y_prime)
    
    if x_prime != 0 and y_prime != 0:
        if x_prime == -1 or y_prime == -1:
            break

        u = random.randint(0,x_prime)
        v = random.randint(0,y_prime)
        w = u*v
        w_prime = util.closest_large_prime_finder(w)
        u_a, u_b = util.two_party_secret_share(u,x_prime)
        v_a, v_b = util.two_party_secret_share(v,y_prime)
        w_a, w_b = util.two_party_secret_share(w,w_prime)
        alice_msg = str(u_a) + ':' + str(v_a) + ':' + str(w_a)
        bob_msg = str(u_b) + ':' + str(v_b) + ':' + str(w_b)
        alice_conn.send(alice_msg.encode())
        bob_conn.send(bob_msg.encode())
        break

serv.close()