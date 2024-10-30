f = open('./55','r')

target = [
  0xCB, 0x84, 0xCC, 0x33, 0xF3, 0xBB, 0x33, 0x45, 0x2C, 0x62, 
  0x84, 0x75, 0x5F, 0xA4, 0xB2, 0xC0, 0x1B, 0xCA, 0x38, 0xAF, 
  0xFA, 0x73, 0x6C, 0xEE, 0x2B, 0x52, 0x5F, 0xF0, 0x54, 0x34, 
  0x49, 0x40, 0x80, 0x45, 0x53, 0x73, 0x02, 0xDF, 0x54, 0xC0, 
  0x33, 0xEC, 0x7D
]
c = f.readline().strip()
formula = {}
for i in range(43):
    formula[i] = f'bvs[{i}]'

while c != '' :
    b = c.split(' ')
    dst = int(b[0])
    op = b[1]
    src1 = int(b[2])
    src2 = int(b[4])
    c = f.readline().strip()
    if op == '+=' :
        formula[dst] = f'({formula[dst]}  + {formula[src1]} + {formula[src2]}) '
    else :
        formula[dst] = f'({formula[dst]}  - {formula[src1]} - {formula[src2]})'

from z3 import *
bvs = [z3.BitVec(f'bvs[{i}]',8) for i in range(0x2b)]
s = Solver()
for bv in bvs:
    s.add(z3.And(bv>=0x20, bv <= 0x7e))


for i in range(len(formula)) :
    print(f'{formula[i]} == {target[i]}')
    s.add(eval(f'{formula[i]} == {target[i]}'))



print(s.check())
print(s.model())
flag = ''
for bv in bvs:
    flag += chr(s.model()[bv].as_long())
print(flag) #AIS3{4r3_yOu_@_sTA7EfUl_OR_ST4T3LESs_CTf3r}