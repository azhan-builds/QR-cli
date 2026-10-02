import qrcode
import argparse
from pathlib import Path
from qrcode.image.svg import SvgPathImage
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops, ImageDraw
import base64
from io import BytesIO

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

def add_logo(image, logo_path, background_color):
    logo = Image.open(logo_path).convert("RGBA")
    rgb_logo = logo.convert("RGB")
    background = Image.new("RGB", rgb_logo.size, rgb_logo.getpixel((0, 0)))
    difference = ImageChops.difference(rgb_logo, background)
    mask = difference.convert("L")
    mask = mask.point(lambda value: 255 if value > 15 else 0)
    bbox = mask.getbbox()
    if bbox:
        logo = logo.crop(bbox)
        mask = mask.crop(bbox)
        logo.putalpha(mask)
    image = image.convert("RGBA")
    logo_size = int(image.width * 0.14)
    logo.thumbnail((logo_size, logo_size))

    padding = int(logo_size * 0.18)
    badge_width = logo.width + padding * 2
    badge_height = logo.height + padding * 2
    badge = Image.new("RGBA", (badge_width, badge_height), background_color)

    mask = Image.new("L", (badge_width, badge_height), 0)
    draw = ImageDraw.Draw(mask)
    radius = int(min(badge_width, badge_height)*0.2)
    draw.rounded_rectangle((0, 0, badge_width, badge_height), radius=radius, fill=255)
    badge.putalpha(mask)
    logo_position = ((badge_width - logo.width)//2, (badge_height - logo.height)//2)
    badge.paste(logo, logo_position, logo)
    badge_position = ((image.width - badge.width)//2, (image.height - badge.height)//2)
    image.paste(badge, badge_position, badge)
    return image

def prepare_logo(logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    rgb_logo = logo.convert("RGB")
    background = Image.new("RGB", rgb_logo.size, rgb_logo.getpixel((0, 0)))
    difference = ImageChops.difference(rgb_logo, background)
    mask = difference.convert("L")
    mask = mask.point(lambda value: 255 if value > 15 else 0)
    bbox = mask.getbbox()
    if bbox:
        logo = logo.crop(bbox)
        mask = mask.crop(bbox)
        logo.putalpha(mask)
    return logo

def add_logo_svg(image, logo_path, background_color):
    logo = prepare_logo(logo_path)
    logo_data = BytesIO()
    logo.save(logo_data, format="PNG")
    encoded_logo = base64.b64encode(logo_data.getvalue()).decode("ascii")
    svg_namespace = "http://www.w3.org/2000/svg"
    view_box = image._img.get("viewBox")
    _, _, svg_width, svg_height = view_box.split()
    svg_width = float(svg_width)
    svg_height = float(svg_height)
    logo_size = svg_width * 0.14
    padding = logo_size * 0.18
    badge_size = logo_size + padding * 2
    badge_x = (svg_width - badge_size) / 2
    badge_y = (svg_height - badge_size) / 2

    badge = ET.Element(f"{{{svg_namespace}}}rect", x=str(badge_x), y=str(badge_y), width=str(badge_size), height=str(badge_size), rx=str(badge_size * 0.2), fill=background_color if background_color != "transparent" else "white")
    image._img.append(badge)

    logo_x = (svg_width - logo_size) / 2
    logo_y = (svg_height - logo_size) / 2
    logo_element = ET.Element(f"{{{svg_namespace}}}image", x=str(logo_x), y=str(logo_y), width=str(logo_size), height=str(logo_size), href=f"data:image/png;base64,{encoded_logo}")
    image._img.append(logo_element)
    return image


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
    parser.add_argument("--color", default="black", help="QR foregound color")
    parser.add_argument("--background", default="white", help="QR background color")
    parser.add_argument("--logo", help="enter path to the logo image")

    args = parser.parse_args()
    if args.scale < 1:
        parser.error("Scale must be at least 1")
    if args.border < 0:
        parser.error("Border cannot be negative")

    if args.logo and not args.output:
        parser.error("--logo requires --output")
    if args.logo and not Path(args.logo).is_file():
        parser.error("logo file does not exist")
    inputs = [args.data, args.text, args.url]
    provided_inputs = [value for value in inputs if value is not None]

    if len(provided_inputs) == 0:
        parser.error("please provide text or a URL")
    if len(provided_inputs) > 1:
        parser.error("please provide only one input")
    data = provided_inputs[0]

    if args.logo:
        args.error_correction = "H"
        if args.scale == 1:
            args.scale = 20

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
        if output_path.suffix.lower() == ".svg":
            image = qr.make_image(image_factory=SvgPathImage, fill_color=args.color)
            image.path.set("fill", args.color)
            if args.background != "transparent":
                background = ET.Element("rect", fill=args.background, x="0", y="0", width="100%", height="100%")
                image._img.insert(0, background)
            if args.logo:
                image = add_logo_svg(image, args.logo, args.background)
        else:
            image = qr.make_image(fill_color=args.color, back_color=args.background)
            if args.logo:
                image = add_logo(image, args.logo, args.background)
        image.save(output_path)
        print(f"QR code saved to {output_path}")
    else:
        matrix = qr.get_matrix()
        matrix = scale_matrix(matrix, args.scale)
        print_qr(matrix, args.style)

if __name__ == "__main__":
    main()  