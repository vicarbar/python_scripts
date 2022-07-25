# Script para generar codigos qr desde python. En el ejemplo, el código qr generado lleva a la página home de twitter.

import qrcode
qr_img = qrcode.make("https://twitter.com/home")
qr_img.save("qrTwitter.png")