guess = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQR'
flag_enc = '6ct69GHt_A00utACToohy_0u0rb_9c5byF3A}G515buR11_kL{3rp_'
guess_enc = 'LyqON3olxPwIcvMbgkhHzumnrsAfQGadF0e2RjJpE765t8K914BCDi'

flag = ''
for i in range(len(guess)):
    flag += flag_enc[guess_enc.find(guess[i])]

print(flag)
