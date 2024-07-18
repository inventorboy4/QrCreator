import argparse
import os
import sys
import qrcode
from qrcode.image.styledpil import StyledPilImage
from PIL import Image

parser = argparse.ArgumentParser(description='QR code image maker')
parser.add_argument('-i', '--input', type=str, help='Path to input *.txt file')
parser.add_argument('-o', '--out', type=str, default='qr_code.png',
                    help='Name of the image output file (default: qr_code.png)')
parser.add_argument('--logo', type=str, help='Path to embedded image file (default: None)')
args = parser.parse_args()
try:
    if not args.input:
        raise Exception('Empty iinput value. -i or --in argument for input file path required.')
    f = open(args.input, encoding='utf-8', mode="r")
    data = f.read()
    if len(data) > 516:
        raise Exception('Input file too big. Please use less than 516 characters.')
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)
    if args.logo:
        image = Image.open(args.logo)
        new_image = Image.new("RGBA", image.size, "WHITE")
        new_image.paste(image, (0, 0), image)
        new_image.convert('RGB').save('edited_logo.jpg', "JPEG")
        img = qr.make_image(image_factory=StyledPilImage,
                            embeded_image_path='edited_logo.jpg')
        os.remove('edited_logo.jpg')
    else:
        img = qr.make_image()
    img.save(args.out)
except Exception as err:
    print(err)
    # input("Press Enter to continue...")
    sys.exit(1)
	 
