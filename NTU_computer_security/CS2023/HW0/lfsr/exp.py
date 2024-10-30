from sage.all import *
from sage.matrix.berlekamp_massey import berlekamp_massey
flag_prefix = b'FLAG{'
flag_prefix = list(map(int, ''.join(["{:08b}".format(c) for c in flag_prefix])))
flag_sufix = b'}'
flag_sufix = list(map(int, ''.join(["{:08b}".format(c) for c in flag_sufix])))

output = [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0]

#output_prefix = output[:40]

P = PolynomialRing(GF(2), "x")
x = P.gen()
poly = 1 + x ** 2 + x ** 17 + x ** 19 + x ** 23 + x ** 37 + x ** 41 + x ** 53  + x ** 64
poly = x**35 + x**34 + x**32 + x**31 + x**30 + x**29 + x**26 + x**25 + x**23 + x**22 + x**19 + x**17 + x**16 + x**11 + x**10 + x**9 + x**8 + x**7 + x**6 + x + 1
B = companion_matrix(poly, format='bottom')
A = B.inverse()
#print(B * vector(no_xor1))

#b = [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1]

no_xor = output[len(output)-78:len(output)-70]

b=[]
for i in range(len(flag_sufix)):
    b.append(flag_sufix[i] ^ no_xor[i])
print(b)
out = output[len(output)-70:len(output)-35]
print(A * vector(out))
print(output[len(output)-70:len(output)-35])
#print(berlekamp_massey(no_xor))
# print(C ** 71 * vector(no_xor))
# print(A_inverse * vector(no_xor))
# no_xor1 = output[len(output)-65:len(output)-1]
# print(no_xor1)