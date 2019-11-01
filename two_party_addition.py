from Util import Util
util = Util()
import random

x = 24
y = 36
prime = util.closest_large_prime_finder(x) if x > y else util.closest_large_prime_finder(y)
print('Prime: ' + str(prime))

x_a, x_b = util.two_party_secret_share(x)
y_a, y_b = util.two_party_secret_share(y)

s_a = x_a + y_a
s_b = x_b + y_b
s = (s_a + s_b)
print('Result of secure computation: ' + str(s))
print('Result of simple addition: ' + str(x+y))