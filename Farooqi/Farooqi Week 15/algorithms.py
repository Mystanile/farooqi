N  = int(input("Enter a number: "))
divisors = []
D = 1
other = []
while D < N:
    if N % D == 0:
        divisors.append(D)
    else: 
        other.append(D)
    D=D+1
print(divisors)
print(other)