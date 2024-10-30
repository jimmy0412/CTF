hint = [3867643078, 3287416726, 901811051, 2873881227, 2270268909, 1555321936, 1419723682, 135531391, 1648732744, 2346142192, 1505498859, 2103436123, 4202619523, 2326904236, 1938136472, 366121018, 773968139, 2415223764, 490067400, 1902082872]
muls = [784927, 1022769, 932825, 746975, 815007, 613147, 537543, 852211, 618443, 866769, 910981, 825227, 838133, 1027271, 776063, 1038141, 571529, 664495, 1025729, 593197]
mods = [2286703839, 2358297603, 3964421567, 3907762623, 2849800663, 2382674777, 2503252379, 2798053355, 3995552795, 2910773165, 3724203063, 2416156797, 2179309517, 3641528223, 2846518171, 2688752197, 4248246955, 2871652981, 2639686887, 4182550363]


def total_13(a):
    b = 0 
    for i in range(len(a)):
        b = b ^ a[i]
    return b

hint_total = total_13(hint)
muls_total = total_13(muls)
mods_total = total_13(mods)


hint_ori = [i ^ hint_total  for i in hint]
muls_ori = [i ^ muls_total  for i in muls]
mods_ori = [i ^ mods_total  for i in mods]

mul = 1 
for i in mods:
    mul = mul * i

from sage.all import crt
from Crypto.Util.number import long_to_bytes
remain = []
for i in range(len(muls)):
    a = hint_ori[i] * pow(muls_ori[i], -1 ,mods_ori[i]) % mods_ori[i]
    remain.append(a)

flag = crt(remain,mods_ori)
print(long_to_bytes(flag))