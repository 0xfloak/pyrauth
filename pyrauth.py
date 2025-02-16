import io
import argparse
import readchar

import pyotp
import qrcode
from qrcode.image.pure import PyPNGImage


def main(name, image_out, static_uri):
    if static_uri:
        totp = pyotp.parse_uri(static_uri)
        uri = static_uri
    else:
        key = pyotp.random_base32()
        totp = pyotp.totp.TOTP(key)
        uri = totp.provisioning_uri(name=name, issuer_name="pyrauth")

    print(f'{"#" * 8} ·~ TOTP URL ~· {"#" * (len(uri) - 24)}')
    print(uri)
    print("#" * len(uri))

    qr = qrcode.QRCode()
    qr.add_data(uri)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())

    if image_out:
        qrcode.make(uri, image_factory=PyPNGImage).save(image_out)
        print(f"Saved to {image_out}")

    while True:
        print(f"Verification code: {totp.now()}")
        print("ENTER for refresh, anything else to exit>")

        if readchar.readchar() != "\n":
            break


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="The name to label the TOTP with")
    parser.add_argument("--uri", help="Use a premade URI", nargs="?")
    parser.add_argument(
        "-o",
        "--output-file",
        help="File to write PNG image to",
        nargs="?",
        type=argparse.FileType("w"),
    )
    return parser.parse_args()


def banner():
    print(
        """
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░
░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓████████▓▒░
░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░
"""
    )


if __name__ == "__main__":
    args = parseargs()
    banner()

    out_file = args.output_file.name if args.output_file else None
    main(args.name, out_file, args.uri)
