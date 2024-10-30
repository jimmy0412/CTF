from PIL import Image, ImageColor
#https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

im = Image.new('RGB', (600,600))


f = open('./qqq','rb')
a = f.read()
rgb = []
for i in range(0,len(a),4):
    b = a[i:i+3]
    c = b[::-1]
    rgb.append(hex_to_rgb(c.hex()))

for i in range(600):
    for j in range(600):
        im.putpixel((j,i),rgb[600*j+i])

im.save('./88.png','png')

