A small command line tool that can help generate QR codes. 

This tool is built with python. It let's you create QR codes and save them as images. You can customize their appearance, add a logo, and generate multiple QR codes from a text file.

I made this project so i can understand and learn more about Python, cmd tools, and more. 

## Preview
![QR-cli generating a QR code](https://user-cdn.hackclub-assets.com/01a13d3c-bcaa-772c-87e8-5d407ff80dc7/1.png)

## Features
-Generate qr code from text and urls
-Display qr codes in the terminal
-Option to choose between compact and block based style
-Adjust the size of the qr and its border
-choose an error correction level
-export qr codes as png or svg files
-Customize foreground and background colors
-Add a logo
-bulk qr generation from a text file

## Installation

Install QR-cli using pip:

```bash
python -m pip install qrcli-toolkit
```

Once installed, run QR-cli directly from your terminal:

```bash
qr --help
```

Generate your first QR code:

```bash
qr "Hello, world!"
```

To upgrade QR-cli:

```bash
python -m pip install --upgrade qrcli-toolkit
```

### Running from source

If you want to explore or modify the code, clone the repository:

```bash
git clone https://github.com/azhan-builds/QR-cli.git
cd QR-cli
python -m pip install "qrcode[pil]"
python qr.py "Hello, world!"
```

## Usage
### Generate a qr code
Pass text or a URL as a positional argument
```bash
python qr.py "Hello, world!"
python qr.py "https://example.com"
```

You can also use the input options:
```bash
python qr.py --text "Hello, world!"
python qr.py --url "https:/example.com"
```

Make sure to provide only one input method at a time

###Terminal styles
This tool has two terminal styles:
```bash
python qr.py "hello" --style compact
python qr.py "hello" --style blocks
```

`compact` is the default style and uses unicode characters
`blocks` uses larger block characters

### Scale and border
Change the size of the qr and its border

```bash
python qr.py "https://example.com" --scale 2
python qr.py "https://example.com" --border 6
python qr.py "https://example.com" --scale 2 --border 6
```

The scale controls the size of the rendering while the border controls the quiet zone width around the qr code

### Error correction
This tool supports all 4 standard error correction levels

```bash
python qr.py "https://example.com" --error-correction L
python qr.py "https://example.com" --error-correction M
python qr.py "https://example.com" --error-correction Q
python qr.py "https://example.com" --error-correction H
```
Higher error correction lets a qr code tolerate more damage but it makes the qr code more dense. This tool uses 'M' by default. Exporting with a logo uses 'H' automatically

### Save a qr code

Export a QR code as PNG"
```bash
python qr.py "https://example.com" --output example.png
```

or export it as SVG:
```bash
python qr.py "https://example.com" --output example.svg
```

The output extenstion lets you determine the image format. If you provide a filename without specifying the path, the image is saved in the systems Download folder. You can also specify a path

### Customize color
Choose a foreground and background color:
```bash
python qr.py "https://example.com" --color green --background white --output example.png
```

For svg output, you can also use a transparent background:
```bash
python qr.py "https://example.com" --background transparent --output example.png
```

The colors must be supported by the image library

### Add a logo

You can place a logo in the center of the code:
```bash
python qr.py "https://example.com" --logo logo.png --output example.png
```

svg output:
```bash
python qr.py "https://example.com" --logo logo.png --output example.svg
```

This tool uses high correction when a logo is added.
keep in mind that a logo can make a qr code harder to scan.

### Read input from a pipe

QR-cli can read text from standard input when no other input option is provided:

```bash
echo "Hello from the terminal" | python qr.py
```

This is useful when you want to pass the output of another command directly into QR-cli.

### Generate multiple QR codes
This tool let's you create multiple qr codes using a text file that containining one input per line. 

Suppose you have a text file, `urls.txt`:
```text
https://example.com
https://kinetiqnrl.com
Hiiii
```

Run:
```bash
python qr.py --file urls.txt
```

by default, the qr codes are saved in:
```text
~/Downloads/qr-codes
```

You can specify a path or directory
```bash
python qr.py --file urls.txt --output generated-codess
```
Each non empty line in the file is treated as an input. Empty lines are skipped. This tool also generates names for each of the code. 

This feature is only available for PNG export only, for now.

## Help
Run:
```bash
python qr.py -help
```

## built with

- Python - for command line logic and input handling
- qrcode - to generate qr codes
- Pillow - to process images and handles png output
- ElementTree - svg element handline

## AI-use disclosure

AI tools were used to assist with parts of the implementation, debugging, and development process. I worked through the features, tested changes, and used the project as an opportunity to learn more about Python and building command-line tools.

## License

QR-cli is licensed under the MIT License. See [LICENSE](LICENSE) for details.