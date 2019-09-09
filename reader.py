import base64
import time
import zlib

import pyperclip
import zxing
from PIL import ImageGrab


def main():
    while True:
        im = ImageGrab.grab()
        im.save('temp.png')
        zx = zxing.BarCodeReader()
        code = zx.decode('temp.png', )
        if code and code.raw:
            text = bytes.decode(zlib.decompress(base64.b64decode(code.raw)), 'utf-8')
            print(text)
            pyperclip.copy(text)
        time.sleep(.5)


if __name__ == '__main__':
    main()
