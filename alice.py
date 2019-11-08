import socket
from Util import Util
util = Util()
import time

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1',8081))
serv.listen(1)

trusted_initializer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
trusted_initializer.connect(util.server_address_builder())

desired_input = input('Please input an integer: \n')
desired_operation = input('Secure Two-party Computation for addition or multiplication (a/m): \n')
x = int(desired_input)
prime = util.closest_large_prime_finder(x)
x_a, x_b = util.two_party_secret_share(x,prime)

bob_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bob_client.connect(('127.0.0.1',8082))
bob_client.send(str('x_b:' + str(x_b)).encode())

if desired_operation == 'a':
    trusted_initializer.send('x_prime:-1'.encode())
    initialized_share = str(trusted_initializer.recv(1024).decode())
    y_a = -1
    bob_sub_addition = -1
    bob_addition = -1
    while True:
        bob_conn, addr = serv.accept()
        data = str(bob_conn.recv(4096).decode())
        if data.split(':')[0] == 'y_a':
            bob_client.close()
            bob_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bob_client.connect(('127.0.0.1',8082))

            y_a = int(data.split(':')[1])
            print('y_a:'+str(y_a))
            sub_addition = x_a + y_a
            msg = 'sub_addition:' + str(sub_addition)
            print(msg)
            bob_client.sendall(msg.encode())
            print('sent')

        if data.split(':')[0] == 'sub_addition':
            bob_sub_addition = int(data.split(':')[1])
            print('bob_sub_addition:'+str(bob_sub_addition))
            addition = sub_addition + bob_sub_addition
            a_a, a_b = util.two_party_secret_share(addition,util.closest_large_prime_finder(addition))
            print('addition share: ' + str(a_a) + ',' + str(a_b))
            msg = 'addition_share:' + str(a_b)
            bob_client.close()
            bob_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bob_client.connect(('127.0.0.1',8082))
            bob_client.send(msg.encode())

        if data.split(':')[0] == 'addition_share':
            bob_addition = int(data.split(':')[1])
            print('addition share bob sent: ' + str(bob_addition))
            break

if desired_operation == 'm':
    prefix_msg = 'x_prime:' + str(prime)
    trusted_initializer.send(prefix_msg.encode())
    initialized_share = str(trusted_initializer.recv(1024).decode())
    u_a = int(initialized_share.split(':')[0])
    v_a = int(initialized_share.split(':')[1])
    w_a = int(initialized_share.split(':')[2])
    y_a = -1
    d_a = -1
    e_a = -1

    while True:
        bob_conn, addr = serv.accept()
        data = str(bob_conn.recv(4096).decode())

        if data.split(':')[0] == 'y_a':
            bob_client.close()
            bob_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bob_client.connect(('127.0.0.1',8082))

            y_a = int(data.split(':')[1])
            d_a = x_a - u_a
            e_a = y_a - v_a
            msg = 'd_a:' + str(d_a) + ':e_a:' + str(e_a) + ':u_a:' + str(u_a) + ':v_a:' + str(v_a) + ':w_a:' + str(w_a)
            bob_client.sendall(msg.encode())

        if data.split(':')[0] == 'd_b':
            d_b = int(data.split(':')[1])
            e_b = int(data.split(':')[3])
            u_b = int(data.split(':')[5])
            v_b = int(data.split(':')[7])
            w_b = int(data.split(':')[9])

            d = d_a + d_b
            e = e_a + e_b
            u = u_a + u_b
            v = v_a + v_b
            w = w_a + w_b
            
            product = w + u * e + d * v + d * e
            a_a, a_b = util.two_party_secret_share(product,util.closest_large_prime_finder(product))
            print('multiplication share: ' + str(a_a) + ',' + str(a_b))
            msg = 'product:' + str(a_b)

            bob_client.close()
            bob_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bob_client.connect(('127.0.0.1',8082))
            bob_client.sendall(msg.encode())

        if data.split(':')[0] == 'product':
            bob_product = data.split(':')[1]
            print('multiplication share of bob sent: ' + str(bob_product))
            break

trusted_initializer.close()
bob_client.close()