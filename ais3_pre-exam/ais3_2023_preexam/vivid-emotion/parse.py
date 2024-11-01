
a = ''
f = open('parse','a')

while True :
    a = input()
    a = a.replace('g_array','').replace('[','a').replace(']','')
    a = f'x.add({a})\n'
    f.write(a)
    #print(a)

