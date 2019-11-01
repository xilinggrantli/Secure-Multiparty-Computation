import socket
from Util import Util
import random

util = Util()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((util.server_address_builder()))
serv.listen(2)

current_operation = ''

alice_conn = ''
bob_conn = ''

# addition
x_b = -9999
y_a = -9999
x_b_sent = False
y_a_sent = False

s_a = -9999
s_b = -9999
s = s_a + s_b

# multiplication
x_prime = -9999
y_prime = -9999

share_sent = False

u = -1
v = -1
w = -1

u_b = -9999
v_a = -9999

d_a = -9999
d_b = -9999
e_a = -9999
e_b = -9999
d = -9999
e = -9999
de_sent = False

x_multiplication = -1
y_multiplication = -1

while True:
    conn, addr = serv.accept()
    data = str(conn.recv(4096).decode())
    print(data)
    if data.split(':')[0] == 'Alice':
        alice_conn = conn
        if data.split(':')[1] == 'a':
            current_operation = 'a'
            if data.split(':')[2] == 'share':
                x_b = int(data.split(':')[3])
            if data.split(':')[2] == 'result':
                s_a = int(data.split(':')[3])
        if data.split(':')[1] == 'm':
            current_operation = 'm'
            if data.split(':')[2] == 'prime':
                x_prime = int(data.split(':')[3])
                u = random.randint(0,x_prime)
                alice_conn.send(str(u).encode())
            if data.split(':')[2] == 'share':
                x_b = int(data.split(':')[3])
                u_b = int(data.split(':')[4])
            if data.split(':')[2] == 'de':
                d_a = int(data.split(':')[3])
                e_a = int(data.split(':')[4])
            if data.split(':')[2] == 'result':
                x_multiplication = int(data.split(':')[3])

    if data.split(':')[0] == 'Bob':
        bob_conn = conn
        if data.split(':')[1] == 'a':
            current_operation = 'a'
            if data.split(':')[2] == 'share':
                y_a = int(data.split(':')[3])
            if data.split(':')[2] == 'result':
                s_b = int(data.split(':')[3])
        if data.split(':')[1] == 'm':
            current_operation = 'm'
            if data.split(':')[2] == 'prime':
                y_prime = int(data.split(':')[3])
                v = random.randint(0,x_prime)
                bob_conn.send(str(v).encode())
            if data.split(':')[2] == 'share':
                y_a = int(data.split(':')[3])
                v_a = int(data.split(':')[4])
            if data.split(':')[2] == 'de':
                d_b = int(data.split(':')[3])
                e_b = int(data.split(':')[4])
            if data.split(':')[2] == 'result':
                y_multiplication = int(data.split(':')[3])
    
    if current_operation == 'a':
        if y_a != -9999 and not y_a_sent and alice_conn != '' and x_b != -9999:
            alice_conn.send(str(y_a).encode())
            y_a_sent = True

        if x_b != -9999 and not x_b_sent and bob_conn != '' and y_a != -9999:
            bob_conn.send(str(x_b).encode())
            x_b_sent = True

        if s_a != -9999 and s_b != -9999:
            s = s_a + s_b
            alice_conn.send(str(s).encode())
            bob_conn.send(str(s).encode())
            print('Result of addition: ' + str(s_b))
            x_b = -9999
            y_a = -9999
    
    if current_operation == 'm':
        if u != -1 and v != -1:
            w = u*v
        
        if not share_sent and x_b != -9999 and u_b != -9999 and y_a != -9999 and v_a != -9999:
            alice_msg = str(y_a) + ':' + str(v_a)
            bob_msg = str(x_b) + ':' + str(u_b)
            alice_conn.send(alice_msg.encode())
            bob_conn.send(bob_msg.encode())
            share_sent = True
        
        if d_a != -9999 and d_b != -9999 and e_a != -9999 and e_b != -9999:
            d = d_a + d_b
            e = e_a + e_b
        
        if not de_sent and w != -1 and u != -1 and v != -1 and d != -9999 and e != -9999:
            msg = str(w) + ':' + str(u) + ':' + str(v) + ':' + str(d) + ':' + str(e)
            alice_conn.send(msg.encode())
            bob_conn.send(msg.encode())
            de_sent = True
        
        if x_multiplication != -1 and y_multiplication != -1:
            if x_multiplication == y_multiplication:
                print('Alice and Bob got same result for multiplication')
                print('Result of multiplication: ' + str(x_multiplication))
                x_multiplication = -1
                y_multiplication = -1