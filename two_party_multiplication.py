from Util import Util
util = Util()
import random

x = 24
y = 36
#prime = util.closest_large_prime_finder(x) if x > y else util.closest_large_prime_finder(y)
x_prime = util.closest_large_prime_finder(x)
y_prime = util.closest_large_prime_finder(y)
#print('Prime: ' + str(prime))

x_a, x_b = util.two_party_secret_share(x,x_prime)
y_a, y_b = util.two_party_secret_share(y,y_prime)
print('x_a: ' + str(x_a))
print('x_b: ' + str(x_b))
print('y_a: ' + str(y_a))
print('y_b: ' + str(y_b))

u = random.randint(0,x_prime)
v = random.randint(0,y_prime)
w = u*v
print('u: ' + str(u))
print('v: ' + str(v))
print('w: ' + str(w))

u_a, u_b = util.two_party_secret_share(u,x_prime)
v_a, v_b = util.two_party_secret_share(v,y_prime)
print('u_a: ' + str(u_a))
print('u_b: ' + str(u_b))
print('v_a: ' + str(v_a))
print('v_b: ' + str(v_b))

d_a = x_a - u_a
d_b = x_b - u_b
d = d_a + d_b
e_a = y_a - v_a
e_b = y_b - v_b
e = e_a + e_b
print("d: " + str(d))
print("e: " + str(e))

product = w + u * e + d * v + d * e
print('Result of secure computation: ' + str(product))
print('Result of simple multiplication: ' + str(x*y))