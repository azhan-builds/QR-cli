import qrcode

text = input("Enter your URL: ")

qr = qrcode.QRCode()
qr.add_data(text)
qr.make()
qr.print_ascii()