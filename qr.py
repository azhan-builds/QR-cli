import qrcode
import argparse
from pathlib import Path

def scale_matrix(matrix, scale):
    scaled = []
    for row in matrix:
        expanded_row= []
        for cell in row:
            expanded_row.extend([cell] * scale)
        for _ in range(scale):
            scaled.append(expanded_row)
    return scaled

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
    parser.add_argument("--scale", type=int, default=1, help="size of the terminal QR code")
    parser.add_argument("--border", type=int, default=4, help= "size of the QR code border")
    parser.add_argument("--error-correction", choices=["L", "M", "Q", "H"], default="M", help="Qr error correction level")
    parser.add_argument("--output", help="save the QR code as a PNG file")

    args = parser.parse_args()
    if args.scale < 1:
        parser.error("Scale must be at least 1")
    if args.border < 0:
        parser.error("Border cannot be negative")
    inputs = [args.data, args.text, args.url]
    provided_inputs = [value for value in inputs if value is not None]

    if len(provided_inputs) == 0:
        parser.error("please provide text or a URL")
    if len(provided_inputs) > 1:
        parser.error("please provide only one input")
    data = provided_inputs[0]

    error_correction = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H
    }
    

    qr = qrcode.QRCode(error_correction=error_correction[args.error_correction], border=args.border, box_size=args.scale)
    qr.add_data(data)
    qr.make()

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute() and output_path.parent == Path("."):
            output_path = Path.home() /"Downloads"/output_path.name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image = qr.make_image()
        image.save(output_path)
        print(f"QR code saved to {output_path}")
    else:
        matrix = qr.get_matrix()
        matrix = scale_matrix(matrix, args.scale)
        print_qr(matrix, args.style)

if __name__ == "__main__":
    main()  