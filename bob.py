import socket
from Util import Util
util = Util()
import time

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1',8082))
serv.listen(1)

trusted_initializer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
trusted_initializer.connect(util.server_address_builder())

desired_input = input('Please input an integer: \n')
desired_operation = input('Secure Two-party Computation for addition or multiplication (a/m): \n')
y = int(desired_input)
prime = util.closest_large_prime_finder(y)
y_a, y_b = util.two_party_secret_share(y,prime)

alice_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice_client.connect(('127.0.0.1',8081))
alice_client.send(str('y_a:' + str(y_a)).encode())

if desired_operation == 'a':
    trusted_initializer.send('y_prime:-1'.encode())
    initialized_share = str(trusted_initializer.recv(1024).decode())
    x_b = -1
    alice_sub_addition = -1
    alice_addition = -1
    while True:
        alice_conn, addr = serv.accept()
        data = str(alice_conn.recv(4096).decode())
        if data.split(':')[0] == 'x_b':
            alice_client.close()
            alice_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            alice_client.connect(('127.0.0.1',8081))

            x_b = int(data.split(':')[1])
            print('x_b:'+str(x_b))
            sub_addition = x_b + y_b
            msg = 'sub_addition:' + str(sub_addition)
            print(msg)
            alice_client.sendall(msg.encode())
            print('sent')
        
        if data.split(':')[0] == 'sub_addition':
            alice_sub_addition = int(data.split(':')[1])
            print('alice_sub_addition:'+str(alice_sub_addition))
            addition = sub_addition + alice_sub_addition
            b_a, b_b = util.two_party_secret_share(addition,util.closest_large_prime_finder(addition))
            print('addition share: ' + str(b_a) + ',' + str(b_b))
            msg = 'addition_share:' + str(b_a)
            alice_client.close()
            alice_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            alice_client.connect(('127.0.0.1',8081))
            alice_client.send(msg.encode())

        if data.split(':')[0] == 'addition_share':
            alice_addition = int(data.split(':')[1])
            print('addition share of alice sent: ' + str(alice_addition))
            break

if desired_operation == 'm':
    prefix_msg = 'y_prime:' + str(prime)
    trusted_initializer.send(prefix_msg.encode())
    initialized_share = str(trusted_initializer.recv(1024).decode())
    u_b = int(initialized_share.split(':')[0])
    v_b = int(initialized_share.split(':')[1])
    w_b = int(initialized_share.split(':')[2])
    x_b = -1
    d_b = -1
    e_b = -1

    while True:
        bob_conn, addr = serv.accept()
        data = str(bob_conn.recv(4096).decode())

        if data.split(':')[0] == 'x_b':
            alice_client.close()
            alice_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            alice_client.connect(('127.0.0.1',8081))

            x_b = int(data.split(':')[1])
            d_b = x_b - u_b
            e_b = y_b - v_b
            msg = 'd_b:' + str(d_b) + ':e_b:' + str(e_b) + ':u_b:' + str(u_b) + ':v_b:' + str(v_b) + ':w_b:' + str(w_b)
            alice_client.sendall(msg.encode())

        if data.split(':')[0] == 'd_a':
            d_a = int(data.split(':')[1])
            e_a = int(data.split(':')[3])
            u_a = int(data.split(':')[5])
            v_a = int(data.split(':')[7])
            w_a = int(data.split(':')[9])

            d = d_a + d_b
            e = e_a + e_b
            u = u_a + u_b
            v = v_a + v_b
            w = w_a + w_b
            
            product = w + u * e + d * v + d * e
            b_a, b_b = util.two_party_secret_share(product,util.closest_large_prime_finder(product))
            print('multiplication share: ' + str(b_a) + ',' + str(b_b))
            msg = 'product:' + str(b_a)

            alice_client.close()
            alice_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            alice_client.connect(('127.0.0.1',8081))
            alice_client.sendall(msg.encode())

        if data.split(':')[0] == 'product':
            alice_product = data.split(':')[1]
            print('multiplication share of alice sent: ' + str(alice_product))
            break

trusted_initializer.close()
alice_client.close()