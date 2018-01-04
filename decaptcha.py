from PIL import Image
import pytesseract

def decaptcha(image="code.jpg"):
    # 替换列表
    rep = {'O': '0', 'D': '0',
           'I': '1', 'L': '1', 'T': '7',
           'Z': '2',
           'S': '8', 'E': '8', 'A': '8', 'B': '8'
           };
    im = Image.open(image)
    # im = im.convert("L")
    threshold = 54
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    im = im.point(table,'1')
    im = im.crop((0,10, 70, 35))
    captcha = pytesseract.image_to_string(im, config='-psm 7')
    for r in rep:
        text = captcha.replace(r, rep[r])
    print(captcha)
    return captcha

if __name__ == '__main__':
    decaptcha()