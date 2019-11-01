import socket
from Util import Util
util = Util()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(util.server_address_builder())
prefix_msg = 'Bob:'
client.send(prefix_msg.encode())
client.close()

desired_input = input('Please input an integer: \n')
desired_operation = input('Secure Two-party Computation for addition or multiplication (a/m): \n')

y = int(desired_input)
prime = util.closest_large_prime_finder(y)

if desired_operation == 'a':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(util.server_address_builder())
    y_a, y_b = util.two_party_secret_share(y,prime)
    msg = prefix_msg + 'a:share:' + str(y_a)
    client.send(msg.encode())
    x_b = int(str(client.recv(1024).decode()))
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(util.server_address_builder())
    s_b = x_b + y_b
    msg = prefix_msg + 'a:result:' + str(s_b)
    client.send(msg.encode())
    addition = int(str(client.recv(1024).decode()))
    client.close()
    print('Result of addition: ' + str(addition))

if desired_operation == 'm':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(util.server_address_builder())
    msg = prefix_msg + 'm:prime:' + str(prime)
    client.send(msg.encode())
    v = int(str(client.recv(1024).decode()))
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(util.server_address_builder())
    y_a, y_b = util.two_party_secret_share(y,prime)
    v_a, v_b = util.two_party_secret_share(v,prime)
    msg = prefix_msg + 'm:share:' + str(y_a) + ':' + str(v_a)
    client.send(msg.encode())
    shared_msg = str(client.recv(1024).decode())
    x_b = int(shared_msg.split(':')[0])
    u_b = int(shared_msg.split(':')[1])
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(util.server_address_builder())
    d_b = x_b - u_b
    e_b = y_b - v_b
    msg = prefix_msg + 'm:de:' + str(d_b) + ':' + str(e_b)
    client.send(msg.encode())
    all_msg = str(client.recv(1024).decode())
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(util.server_address_builder())
    w = int(all_msg.split(':')[0])
    u = int(all_msg.split(':')[1])
    v = int(all_msg.split(':')[2])
    d = int(all_msg.split(':')[3])
    e = int(all_msg.split(':')[4])
    product = w + u * e + d * v + d * e
    msg = prefix_msg + 'm:result:' + str(product)
    client.send(msg.encode())
    print('Result of multiplication: ' + str(product))

client.close()