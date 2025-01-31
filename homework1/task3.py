def odd_or_even(input):
    if input == 0:
        print("Zero")
    elif input % 2 == 0:
        print("Even")
    else:
        print("Odd")
    
def get_primes():
    # Prime-finding code taken from GeeksForGeeks
    primes = []
    
    # Function to generate N prime numbers using  
    # Sieve of Eratosthenes 
    def SieveOfEratosthenes():
        
        n = 100
        
        # Create a boolean array "prime[0..n]" and 
        # initialize all entries it as true. A value
        # in prime[i] will finally be false if i is 
        # Not a prime, else true. 
        prime = [True for i in range(n + 1)] 
        
        p = 2
        while (p * p <= n): 
            
            # If prime[p] is not changed, 
            # then it is a prime 
            if (prime[p] == True): 
                
                # Update all multiples of p 
                for i in range(p * p, n + 1, p): 
                    prime[i] = False
                    
            p += 1
        
        # Print all prime numbers 
        for p in range(2, n + 1): 
            if prime[p]: 
                primes.append(p) 
        

    SieveOfEratosthenes()
    for i in range(10):
        print(primes[i])

def sums():
    sum = 0
    index = 1
    limit = 100
    while index < limit:
        sum += index
        index += 1
    return sum

if __name__ == "__main__":
    odd_or_even(0)
    get_primes()
    print(sums())
