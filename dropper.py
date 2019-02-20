import base64
import threading
import time
import tkinter
import zlib

import pyperclip
import qrcode
from PIL import ImageTk

window: tkinter.Tk = None


def main():
    global window
    window = tkinter.Tk()
    window.overrideredirect(True)
    window.wm_attributes("-topmost", True)
    window.wm_attributes("-disabled", True)
    window.wm_attributes("-alpha", 1)

    threading.Thread(target=watch_clipboard).start()

    window.mainloop()


def watch_clipboard():
    recent_value = ''
    while True:
        tmp_value = pyperclip.paste()
        if tmp_value != recent_value:
            recent_value = tmp_value
            print(recent_value)

            # label = tkinter.Label(text=recent_value)
            # label.pack()

            qr_code = get_qr_code(base64.b64encode(zlib.compress(recent_value.encode('utf-8'))))

            img_tk = ImageTk.PhotoImage(qr_code)

            show_image(img_tk)

        time.sleep(1)


def get_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=0,
    )
    qr.clear()
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def show_image(img_tk):
    global window

    label = tkinter.Label(window, image=img_tk)
    label.pack()

    window.deiconify()

    label.after(2000, destroy_widget, label)


def destroy_widget(widget):
    widget.destroy()
    window.withdraw()


if __name__ == '__main__':
    main()
