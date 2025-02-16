import io
import argparse
import readchar

import pyotp
import qrcode
from qrcode.image.pure import PyPNGImage


def main(share_name, local_name, image_out, static_uri, non_interactive):
    if static_uri:
        totp = pyotp.parse_uri(static_uri)
    else:
        key = pyotp.random_base32()
        totp = pyotp.totp.TOTP(key)

    local_uri = totp.provisioning_uri(name=local_name, issuer_name="PYRauth")
    share_uri = totp.provisioning_uri(name=share_name, issuer_name="PYRauth")

    print_uri(local_uri, "LOCAL URI (FOR YOU)")

    if not non_interactive:
        print("Add this to your own authenticator app.")
        print("Then press any key to view share URI (labeled for friend)")
        readchar.readchar()
        print()
        print()

    print_uri(share_uri, "SHARE URI (FOR FRIEND)")

    if image_out:
        qrcode.make(share_uri, image_factory=PyPNGImage).save(image_out)
        print(f"Saved to {image_out}")

    if non_interactive:
        return

    while True:
        print(f"Verification code: {totp.now()}")
        print("ENTER for refresh, anything else to exit>")

        if readchar.readchar() != "\n":
            break


def print_uri(uri, title):
    print(f'{"#" * 8} ·~ {title} ~· {"#" * (len(uri) - len(title) - 8 - 8)}')
    print(uri)
    print("#" * len(uri))

    qr = qrcode.QRCode()
    qr.add_data(uri)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("local_name", help="The name to label your own TOTP with")
    parser.add_argument("share_name", help="The name your friend will see on their TOTP key")
    parser.add_argument("--uri", help="Use a premade URI for the key", nargs="?")
    parser.add_argument(
        "-q", "--non-interactive", help="Don't prompt for input", action="store_true"
    )
    parser.add_argument(
        "-o",
        "--output-file",
        help="File to write PNG image to (share version)",
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
    main(args.share_name, args.local_name, out_file, args.uri, args.non_interactive)
