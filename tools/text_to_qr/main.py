import argparse
import base64
import io

import qrcode


def generate_qr(text):
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)

    # Generate terminal-friendly ASCII art
    print("QR Code Generated")
    print("=" * 40)
    print(f"  Content: {text[:80]}{'...' if len(text) > 80 else ''}")
    print(f"  Length:  {len(text)} characters")
    print("=" * 40)
    print()

    # Print ASCII version
    qr.print_ascii(invert=True)

    # Generate PNG as base64
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    print(f"\nBase64 PNG ({len(b64)} chars):")
    print(b64)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a QR code from text")
    parser.add_argument("text", help="Text or URL to encode as QR code")
    args = parser.parse_args()
    generate_qr(args.text)
