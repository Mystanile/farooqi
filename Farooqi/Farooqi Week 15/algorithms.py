# N  = int(input("Enter a number: "))
# divisors = []
# D = 1
# other = []
# while D < N:
#     if N % D == 0:
#         divisors.append(D)
#     else: 
#         other.append(D)
#     D=D+1
# print(divisors)
# print(other)

# N = int(input("Enter a number greater than or equal to 0: "))
# FACT = 1
# CTRL = 1
# if N <= 0:
#     while CTRL <= N:
#         FACT = FACT * CTRL
#         CTRL = CTRL + 1
#     print(FACT)
# else:
#     print('invalid input')

# def gcdandlcm(A,B):
#     if A > B:
#         N = A
#         D = B
#     else:
#         N = B
#         D = A
#     r = N % D
#     while r != 0:
#         N = D
#         D = r
#         r = N % D
#     return D, (A * B) // D

# A = int(input("Enter a number: "))
# B = int(input("Enter another number: "))
# print(gcdandlcm(A, B))


def prime(NUM):
    if NUM < 2:
        return False
    for i in range(2, int(NUM**0.5) + 1):
        if NUM % i == 0:
            return False
    return True
print(prime(int(input("Enter a number: ")))) 