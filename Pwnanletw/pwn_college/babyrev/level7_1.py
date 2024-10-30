### len=0x1b
### change 7 and 9
### bubblesort -> rev
### change 5 11 
### change 21 22

a = 'zzzyyrwuttsxrnmkjggfedddcca'
b = ''
for i in range(len(a)):
    if i == 5:
        b += a[11]
    elif i == 11:
        b += a[5]
    elif i == 21:
        b += a[22]
    elif i == 22:
        b += a[21]
    else :
        b += a[i]


b = b[::-1]
c = ''
for i in range(len(b)):
    if i == 9:
        c += b[7]
    elif i == 7:
        c += b[9]
    else :
        c += b[i]

print(c)