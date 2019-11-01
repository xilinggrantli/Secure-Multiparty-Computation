import random

class Util:

    def __init__(self):
        pass

    def is_prime(self,n):
        '''
        Check if integer n is a prime or not
        Input: n (Integer)
        Output: bool (True for prime, False for not prime)
        '''
        for i in range(2,n):
            if n % i == 0:
                return False
        return True

    def closest_large_prime_finder(self,n):
        '''
        Find a close prime for integer n, which is just larger than n
        Input: n (Integer)
        Output: a prime integer
        '''
        is_found = False
        prime = n
        while is_found == False:
            if self.is_prime(prime):
                is_found = True
            else:
                prime += 1
        return prime
    
    def two_party_secret_share(self,n,prime):
        '''
        Split secret share for integer n in secure 2-party computation
        Input: n (integer)
               prime (prime number)
        Output: shares n_a and n_b
        '''
        n_a = random.randint(0,n)
        n_b = n - n_a % prime
        return n_a, n_b
    
    def server_address_builder(self):
        return (('127.0.0.1',8080))