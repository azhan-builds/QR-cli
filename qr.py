import qrcode
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate QR codes in your terminal"  )
    parser.add_argument(
        "data",
        nargs="?",
        help="text or URL to encode into QR code"
    )

    parser.add_argument("--text", help="text to encode")
    parser.add_argument("--url", help="URL to encode")

    args = parser.parse_args()
    inputs = [args.data, args.text, args.url]
    provided_inputs = [value for value in inputs if value is not None]

    if len(provided_inputs) == 0:
        parser.error("please provide text or a URL")
    if len(provided_inputs) > 1:
        parser.error("please provide only one input")
    data = provided_inputs[0]

    qr = qrcode.QRCode()
    qr.add_data(args.data)
    qr.make()
    qr.print_ascii()

if __name__ == "__main__":
    main()  