import socket
from Util import Util
util = Util()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(util.server_address_builder())
prefix_msg = 'Alice:'
client.send(prefix_msg.encode())
client.close()

desired_input = input('Please input an integer: \n')
desired_operation = input('Secure Two-party Computation for addition or multiplication (a/m): \n')

x = int(desired_input)
prime = util.closest_large_prime_finder(x)

if desired_operation == 'a':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(util.server_address_builder())
    x_a, x_b = util.two_party_secret_share(x,prime)
    msg = prefix_msg + 'a:share:' + str(x_b)
    client.send(msg.encode())
    y_a = int(str(client.recv(1024).decode()))
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(util.server_address_builder())
    s_a = x_a + y_a
    msg = prefix_msg + 'a:result:' + str(s_a)
    client.send(msg.encode())
    addition = int(str(client.recv(1024).decode()))
    client.close()
    print('Result of addition: ' + str(addition))

if desired_operation == 'm':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(util.server_address_builder())
    msg = prefix_msg + 'm:prime:' + str(prime)
    client.send(msg.encode())
    u = int(str(client.recv(1024).decode()))
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(util.server_address_builder())
    x_a, x_b = util.two_party_secret_share(x,prime)
    u_a, u_b = util.two_party_secret_share(u,prime)
    msg = prefix_msg + 'm:share:' + str(x_b) + ':' + str(u_b)
    client.send(msg.encode())
    shared_msg = str(client.recv(1024).decode())
    y_a = int(shared_msg.split(':')[0])
    v_a = int(shared_msg.split(':')[1])
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(util.server_address_builder())
    d_a = x_a - u_a
    e_a = y_a - v_a
    msg = prefix_msg + 'm:de:' + str(d_a) + ':' + str(e_a)
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
