import qrcode
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate QR codes in your terminal"  )
    parser.add_argument(
        "data",
        nargs="?",
        help="text or URL to encode into QR code"
    )

    args = parser.parse_args()
    if not args.data:
        parser.error("please provide text or a URL")

    qr = qrcode.QRCode()
    qr.add_data(args.data)
    qr.make()
    qr.print_ascii()

if __name__ == "__main__":
    main()  