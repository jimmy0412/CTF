from pwn import *
a = [0x47, 0x56, 0xF8, 0xBE, 0xFD, 0xFB, 0xA6, 0xFB, 0xA7, 0xFF, 
  0xF2, 0xF2, 0x0C, 0x63, 0x33, 0x11, 0x65, 0x2F, 0x18, 0x21, 
  0x69, 0x63, 0x35, 0x25, 0x2D, 0x18, 0x04, 0x7C, 0x1F, 0x22, 
  0x0B, 0x02, 0x26, 0xBC, 0x92, 0x94, 0x53, 0x5E, 0x48, 0x6F, 
  0x4F, 0x5D, 0x40, 0x3E, 0x6D, 0x77, 0x57, 0x3F, 0x01, 0x01, 
  0x00, 0xB1, 0xB5, 0xBA, 0xBA, 0xBA, 0xBA, 0xBA, 0xA7, 0xA7, 
  0xA8, 0xA8, 0xA8, 0xAB, 0xAB, 0xA9, 0x78, 0x78, 0x77, 0x77, 
  0x77, 0x76, 0x76, 0x75, 0xC4, 0xCB, 0xCC, 0xCC, 0xCD, 0xCD, 
  0xCE, 0xCF, 0xCF, 0xCF, 0x30, 0x30, 0x31, 0x31, 0x32, 0x33, 
  0x3A, 0x38, 0x39, 0x8A, 0x8A, 0x89, 0x89, 0x89, 0x88, 0x88, 
  0x88, 0x88, 0x59, 0x5B, 0x5B, 0x5B, 0x59, 0x59, 0x59, 0x27, 
  0x27, 0x57, 0x57, 0x4B, 0x48, 0x48, 0x49, 0x49, 0x4E, 0x4E, 
  0x4F, 0x4B, 0xF9, 0xF9, 0xF8, 0x07, 0x07, 0x05, 0x04, 0x04, 
  0x07, 0x07, 0x06, 0x01, 0x01, 0x00, 0x00, 0x03, 0x01, 0xB0, 
  0xB1, 0xB1, 0xB1, 0xBA, 0xBA, 0xBA, 0xBA, 0xBA, 0xE9, 0xD7, 
  0xD7, 0xA9, 0xA9, 0xA9, 0x78, 0x78, 0x77, 0x77, 0x77, 0x76, 
  0x76, 0xC6, 0xC6, 0xC7, 0xC5, 0xC2, 0xC2, 0xC3, 0xC3, 0xC0, 
  0xC1, 0xC1, 0xC1, 0x3E, 0x3E, 0x3F, 0x3F, 0x3C, 0x3D, 0x3D, 
  0x38, 0x39, 0x39, 0x8A, 0x89, 0x89, 0x89, 0x88, 0x88, 0x88, 
  0x88, 0x88, 0x5B, 0x5B, 0x5B, 0x59, 0x59, 0x59, 0x27, 0x26, 
  0x57, 0x57, 0x48, 0x48, 0x48, 0x49, 0x49, 0x4E, 0x4E, 0x4F, 
  0x4B, 0xF9, 0xF8, 0xF8, 0x07, 0x07, 0x05, 0x04, 0x04, 0x07, 
  0x07, 0x06, 0x01, 0x01, 0x00, 0x00, 0x03, 0x03, 0xB0, 0xB1, 
  0xB1, 0xB1, 0xBE, 0xBE, 0xBA, 0xBA, 0xEB, 0xE9, 0xE9, 0xE9, 
  0xD7, 0xD7, 0x78, 0x78, 0x77, 0x77, 0x77, 0x76, 0xC1, 0xC1, 
  0xC4, 0xC4, 0xC5, 0xC7, 0xC0, 0xC1, 0xC1, 0xC2, 0xC2, 0xC1, 
  0xC1, 0xC1, 0x3E, 0x3E, 0x3F, 0x3C, 0x3E, 0x3F, 0x3F, 0x38, 
  0x3B, 0x3B, 0x3B, 0x89, 0x89, 0x89, 0x88, 0x88, 0x88, 0x88, 
  0x88, 0x5B, 0x5B, 0x59, 0x59, 0x59, 0x59, 0x26, 0x26, 0x57, 
  0x57, 0x48, 0x48, 0x49, 0x49, 0x4E, 0x4E, 0x4F, 0x4F, 0xF9, 
  0xF9, 0xF8, 0xF8, 0x07, 0x07, 0x05, 0x04, 0x04, 0x07, 0x06, 
  0x06, 0x01, 0x01, 0x00, 0x00, 0x03, 0x03, 0xB0, 0xB1, 0xB1, 
  0xB1, 0xBE, 0xBE, 0xBE, 0xBE, 0xEB, 0xEB, 0xEB, 0xE9, 0xE9, 
  0xE9, 0x78, 0x77, 0x77, 0x77, 0x77, 0xC7, 0xC7, 0xC4, 0xC2, 
  0xC3, 0xC3, 0xC2, 0xC2, 0xC3, 0xC3, 0x93, 0x93, 0x92, 0x92, 
  0x92, 0x6D, 0x3C, 0x3D, 0x3E, 0x3E, 0x3F, 0x3F, 0x38, 0x3A, 
  0x3B, 0x3B, 0x3E, 0x89, 0x89, 0x89, 0x88, 0x88, 0x88, 0x88, 
  0x88, 0x5B, 0x59, 0x59, 0x59, 0x58, 0x26, 0x26, 0x57, 0x54, 
  0x48, 0x48, 0x49, 0x49, 0x4E, 0x4E, 0x4F, 0x4F, 0xFB, 0xF9, 
  0xF8, 0x07, 0x07, 0x07, 0x05, 0x04, 0x07, 0x07, 0x06, 0x06, 
  0x01, 0x01, 0x00, 0x00, 0x03, 0x03, 0x03, 0xB1, 0xB1, 0xB1, 
  0xB1, 0xBE, 0xBE, 0xBE, 0xE9, 0xE9, 0xEB, 0xEB, 0xEB, 0xE9, 
  0x17, 0x17, 0x77, 0x77, 0x76, 0xC5, 0xC5, 0xC6, 0xC4, 0xC5, 
  0xC5, 0xC4, 0xC4, 0x94, 0x97, 0x93, 0x92, 0x92, 0x92, 0x92, 
  0x6D, 0x6C, 0x6C, 0x6F, 0x3C, 0x3D, 0x3D, 0x3A, 0x3A, 0x3B, 
  0x3D, 0x3E, 0x3E, 0x89, 0x89, 0x88, 0x88, 0x88, 0x88, 0x88, 
  0x59, 0x59, 0x59, 0x59, 0x58, 0x26, 0x26, 0x57, 0x54, 0x48, 
  0x49, 0x49, 0x49, 0x4E, 0x4E, 0x4F, 0x4C, 0xFB, 0xF8, 0xF8, 
  0x07, 0x07, 0x07, 0x06, 0x04, 0x07, 0x07, 0x06, 0x06, 0x01, 
  0x01, 0x00, 0x00, 0x03, 0x03, 0x03, 0xB1, 0xB1, 0xB1, 0xB1, 
  0xBE, 0xBE, 0xBE, 0xE9, 0xE9, 0xE9, 0xE9, 0xEB, 0xE4, 0x17, 
  0x17, 0x17, 0x16, 0x16, 0xC7, 0xC4, 0xC4, 0xC7, 0xC7, 0xC0, 
  0xC2, 0x94, 0x94, 0x97, 0x97, 0x96, 0x96, 0x96, 0x69, 0x69, 
  0x68, 0x68, 0x6B, 0x6B, 0x3B, 0x3B, 0x3C, 0x3C, 0x3D, 0x3D, 
  0x3E, 0x38, 0x38, 0x89, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 
  0x59, 0x59, 0x58, 0x26, 0x26, 0x26, 0x25, 0x54, 0x48, 0x49, 
  0x49, 0x4E, 0x4E, 0x4F, 0x4F, 0xFB, 0xFB, 0xFA, 0xF8, 0x07, 
  0x07, 0x07, 0x06, 0x04, 0x07, 0x07, 0x06, 0x01, 0x01, 0x00, 
  0x00, 0x00, 0x03, 0x03, 0x02, 0x02, 0xB1, 0xB1, 0xB1, 0xBE, 
  0xBE, 0xBE, 0xBE, 0xEF, 0xEF, 0xE9, 0xE9, 0xE6, 0x17, 0x17, 
  0x17, 0x16, 0x16, 0x39, 0x3A, 0x3A, 0xC5, 0xC5, 0xC2, 0xC0, 
  0x90, 0x90, 0x93, 0x96, 0x96, 0x96, 0x96, 0x69, 0x69, 0x68, 
  0x6B, 0x6B, 0x6A, 0x6A, 0x6D, 0x3C, 0x3C, 0x3D, 0x3D, 0x3E, 
  0x38, 0x38, 0x39, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x59, 
  0x58, 0x58, 0x26, 0x26, 0x26, 0x25, 0x54, 0x49, 0x49, 0x49, 
  0x4E, 0x4E, 0x4F, 0x4F, 0xFB, 0xFA, 0xFA, 0x07, 0x07, 0x07, 
  0x07, 0x06, 0x05, 0x07, 0x06, 0x06, 0x01, 0x01, 0x00, 0x00, 
  0x03, 0x05, 0x05, 0x04, 0x04, 0x04, 0xB5, 0xBA, 0xBA, 0xBE, 
  0xBE, 0xBE, 0xEF, 0xEF, 0xEF, 0xE0, 0xE6, 0x17, 0x17, 0x17, 
  0x16, 0x16, 0x44, 0x44, 0x3A, 0x3B, 0x3B, 0x3C, 0xC2, 0x90, 
  0x93, 0x93, 0x92, 0x92, 0x92, 0x92, 0x6D, 0x68, 0x68, 0x6B, 
  0x6B, 0x6A, 0x6A, 0x6D, 0x6D, 0x3B, 0x3B, 0x3B, 0x38, 0x38, 
  0x38, 0x39, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x58, 
  0x58, 0x26, 0x26, 0x25, 0x25, 0x54, 0x55, 0x49, 0x4E, 0x4E, 
  0x4F, 0x4F, 0x4C, 0xFB, 0xFA, 0xFA, 0x05, 0x07, 0x07, 0x06, 
  0x06, 0x05, 0x05, 0x06, 0x06, 0x01, 0x01, 0x00, 0x00, 0x03, 
  0x03, 0x05, 0x04, 0x04, 0x04, 0x04, 0xBA, 0xBA, 0xBA, 0xBA, 
  0xBA, 0xBA, 0xEF, 0xEF, 0xE0, 0xE0, 0xE0, 0x17, 0x16, 0x16, 
  0x16, 0x15, 0x44, 0x45, 0x45, 0x42, 0x3C, 0x3D, 0x8C, 0x8F, 
  0x93, 0x92, 0x92, 0x92, 0x6D, 0x6D, 0x6C, 0x6C, 0x6F, 0x6F, 
  0x6E, 0x6E, 0x6D, 0x6D, 0x3B, 0x3B, 0x3B, 0x38, 0x38, 0x38, 
  0x3B, 0x3B, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x58, 0x26, 
  0x26, 0x26, 0x25, 0x25, 0x54, 0x55, 0x49, 0x4E, 0x4E, 0x4F, 
  0x4F, 0x4C, 0xFB, 0xFA, 0xFA, 0x05, 0x05, 0x07, 0x06, 0x06, 
  0x05, 0x04, 0x04, 0x01, 0x01, 0x00, 0x00, 0x00, 0x03, 0x03, 
  0x04, 0x04, 0x04, 0x04, 0x0B, 0x0B, 0xBA, 0xBA, 0xBA, 0xBA, 
  0xBA, 0xBA, 0xE9, 0xE6, 0xE0, 0xE0, 0xE0, 0x16, 0x16, 0x16, 
  0x15, 0x15, 0x47, 0x47, 0x40, 0x42, 0x43, 0x43, 0x8F, 0x8E, 
  0x8E, 0x8E, 0x8E, 0x6D, 0x6D, 0x6C, 0x6F, 0x6F, 0x6E, 0x6E, 
  0x69, 0x69, 0x68, 0x68, 0x39, 0x3A, 0x3A, 0x3A, 0x3A, 0x3B, 
  0x3B, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x27, 0x26, 0x26, 
  0x26, 0x25, 0x25, 0x25, 0x55, 0x55, 0x4E, 0x4E, 0x4F, 0x4F, 
  0x4C, 0xFD, 0xFA, 0x05, 0x05, 0x05, 0x05, 0x04, 0x05, 0x05, 
  0x04, 0x04, 0x03, 0x01, 0x00, 0x00, 0x03, 0x03, 0x03, 0x02, 
  0x04, 0x04, 0x0B, 0x0B, 0x0B, 0x0B, 0xBA, 0xBA, 0xBA, 0xBA, 
  0xBA, 0xBA, 0xE6, 0xE6, 0xE6, 0xE6, 0xE7, 0x16, 0x16, 0x15, 
  0x15, 0x45, 0x47, 0x40, 0x40, 0x41, 0x41, 0x40, 0x8E, 0x8E, 
  0x8E, 0x8E, 0x71, 0x70, 0x70, 0x73, 0x6F, 0x6E, 0x6E, 0x69, 
  0x69, 0x68, 0x68, 0x3B, 0x3A, 0x3A, 0x3A, 0x3B, 0x3B, 0x3B, 
  0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x88, 0x26, 0x26, 0x26, 
  0x25, 0x25, 0x25, 0x55, 0x55, 0x4E, 0x4E, 0x4F, 0x4F, 0x4C, 
  0xFC, 0xFC, 0x05, 0x05, 0x05, 0x04, 0x04, 0x07, 0x05, 0x04, 
  0x04, 0x03, 0x03, 0x00]

f = open(b'./data','rb')
b = f.read()

c = []
for i in range(1024):
  c.append(b[i] ^ a[i])
print(bytes(c))

# r = process('./donut-verifier')
# input()
# r.sendline(b'\x00'*1023)

# r.interactive()