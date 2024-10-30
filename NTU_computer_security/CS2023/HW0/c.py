
from Crypto.Util.number import bytes_to_long, getPrime

def xorrrrr(nums):
    n = len(nums)
    result = [0] * n
    for i in range(1, n):
        result = [ result[j] ^ nums[(j+i) % n] for j in range(n)]
        
    return result

# a = [132,456,789,234,564,1233]
# b = xorrrrr(a)
# print(b)


# def total_13(a):
#     b = 0 
#     for i in range(len(a)):
#         b = b ^ a[i]
#     return b

# c = total_13(b)
# print(c)
# hint_ori = [i ^ c  for i in b]
# print(hint_ori)
secret = bytes_to_long(flag)
mods = [ getPrime(32) for i in range(20)]
muls = [ getPrime(20) for i in range(20)]

hint = [secret * muls[i] % mods[i] for i in range(20)]

print(f"hint = {xorrrrr(hint)}")
print(f"muls = {xorrrrr(muls)}")
print(f"mods = {xorrrrr(mods)}")

# hint = [3867643078, 3287416726, 901811051, 2873881227, 2270268909, 1555321936, 1419723682, 135531391, 1648732744, 2346142192, 1505498859, 2103436123, 4202619523, 2326904236, 1938136472, 366121018, 773968139, 2415223764, 490067400, 1902082872]
# muls = [784927, 1022769, 932825, 746975, 815007, 613147, 537543, 852211, 618443, 866769, 910981, 825227, 838133, 1027271, 776063, 1038141, 571529, 664495, 1025729, 593197]
# mods = [2286703839, 2358297603, 3964421567, 3907762623, 2849800663, 2382674777, 2503252379, 2798053355, 3995552795, 2910773165, 3724203063, 2416156797, 2179309517, 3641528223, 2846518171, 2688752197, 4248246955, 2871652981, 2639686887, 4182550363]
