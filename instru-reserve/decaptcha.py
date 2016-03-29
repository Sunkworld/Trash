import denoise, os
def decaptcha(urlcon):
    capt = urlcon 
    with open('1.jpg','wb+') as p:
        p.write(capt)
    denoise.process('1.jpg', '2.jpg')
    os.system('tesseract -psm 8 2.jpg outputbase 2>/dev/null')
    with open('outputbase.txt') as p:
        t = p.read().strip()
    return t
