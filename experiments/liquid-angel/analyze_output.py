
import sympy

def analyze_angel_output(numbers):
    print(f"Analyzing Output Sequence: {numbers}")
    
    for num in numbers:
        n = int(num)
        is_prime = sympy.isprime(n)
        factors = sympy.factorint(n) if not is_prime else "PRIME"
        
        # Enochian Gematria (Simple Sum of Digits for now, or Modulo 9)
        # 3-6-9 Harmonics check
        mod9 = n % 9
        
        # Prime Factorization Gematria?
        # If factors sums to something meaningful?
        
        print(f"Num: {n:4d} | Prime: {str(is_prime):5s} | Mod9: {mod9} | Factors: {factors}")

if __name__ == "__main__":
    # Outputs from the session
    outputs = [
        [112, 199, 1744, 198, 100, 692, 158, 1682, 101, 88], # Primes Prompt
        [199, 521, 107, 458, 102], # Self x Void
        [100, 100, 508, 683, 714], # Void Gate
        [89, 599, 1666, 937, 1461, 126, 890, 227, 1250, 617, 1541, 157, 1790, 100, 1029, 1009, 1826, 159, 1670, 138] # Self x Self
    ]
    
    for seq in outputs:
        print("-" * 40)
        analyze_angel_output(seq)
