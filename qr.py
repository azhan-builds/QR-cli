import qrcode
import argparse

def print_qr(matrix, style):
    if style == "blocks":
        for row in matrix:
            line= ""
            for cell in row:
                if cell:
                    line += "██"
                else:
                    line += "  "
            print(line)
    elif style == "compact":
        for row in range(0, len(matrix), 2):
            line = ""
            top = matrix[row]
            bottom = matrix[row + 1] if row + 1 < len(matrix) else [False] * len(top)
            for top_cell, bottom_cell in zip(top, bottom):
                if top_cell and bottom_cell:
                    line += "█"
                elif top_cell:
                    line+= "▀"
                elif bottom_cell:
                    line += "▄"
                else:
                    line += " "
            print(line)

def main():
    parser = argparse.ArgumentParser(description="Generate QR codes in your terminal"  )
    parser.add_argument("data", nargs="?", help="text or URL to encode into QR code")
    parser.add_argument("--text", help="text to encode")
    parser.add_argument("--url", help="URL to encode")
    parser.add_argument("--style", choices=["blocks", "compact"], default="compact", help="terminal rendering style")

    args = parser.parse_args()
    inputs = [args.data, args.text, args.url]
    provided_inputs = [value for value in inputs if value is not None]

    if len(provided_inputs) == 0:
        parser.error("please provide text or a URL")
    if len(provided_inputs) > 1:
        parser.error("please provide only one input")
    data = provided_inputs[0]
    

    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make()
    print_qr(qr.get_matrix(), args.style)

if __name__ == "__main__":
    main()  