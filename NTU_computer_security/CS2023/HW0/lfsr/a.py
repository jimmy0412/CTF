
from Crypto.Util.number import bytes_to_long
from os import urandom

class LFSR:
    def __init__(self, tap, state):
        self._tap = tap
        self._state = state

    def getbit(self):
        f = sum([self._state[i] for i in self._tap]) & 1
        x = self._state[0]
        self._state = self._state[1:] + [f]
        return x
FLAG = b'FLAG{123}'
flag = list(map(int, ''.join(["{:08b}".format(c) for c in FLAG])))
key = [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1]
taps = [0, 2, 17, 19, 23, 37, 41, 53]
randomness = LFSR(taps, key)

output = []
a = []
for _ in range(len(flag) + 70):
    for __ in range(70):
        x = randomness.getbit()
        a.append(x)
    b = randomness.getbit()
    output.append(b)
    a.append(b)

# for i in range(len(flag)):
#     output[i] ^= flag[i]

# print(output)
# print(a)