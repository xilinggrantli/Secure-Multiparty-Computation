class Util:

    def __init__(self):
        pass

    def is_prime(self,n):
        for i in range(2,n):
            if n % i == 0:
                return False
        return True

    def closest_large_prime_finder(self,n):
        is_found = False
        prime = n
        while is_found == False:
            if self.is_prime(prime):
                is_found = True
            else:
                prime += 1
        return prime