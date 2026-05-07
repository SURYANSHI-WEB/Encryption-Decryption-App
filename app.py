from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image
from typing import cast, Tuple
import io

app = Flask(__name__)
CORS(app)  # Allow requests from the browser (different port)


# ── Helper: convert text to binary string ─────────────────────────────────────
# Example: "Hi" → "0100100001101001"
def text_to_binary(text):
    binary = ""
    for char in text:
        binary += format(ord(char), '08b')  # each char → 8 bits
    return binary


# ── Helper: convert binary string back to text ────────────────────────────────
# Example: "01001000" → "H"
def binary_to_text(binary):
    text = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:  # skip incomplete bytes at the end
            text += chr(int(byte, 2))
    return text


# ── Route: Hide a message inside an image ─────────────────────────────────────
@app.route('/api/hide', methods=['POST'])
def hide_text():
    image_file  = request.files['image']
    secret_text = request.form['message'] + "#####"  # ##### marks where message ends

    # Open image and convert to RGB (removes any alpha channel)
    img = Image.open(image_file.stream).convert('RGB')
    width, height = img.size

    # Convert the secret text to 1s and 0s
    binary_message = text_to_binary(secret_text)
    total_bits = len(binary_message)

    # Check if the image is big enough to hold the message
    # Each pixel stores 1 bit (in the red channel)
    if total_bits > width * height:
        return jsonify({'error': 'Message is too long for this image'}), 400

    bit_index = 0

    # Go through pixels one by one and hide one bit in each red value
    for y in range(height):
        for x in range(width):
            if bit_index < total_bits:
                # cast tells Pylance the pixel is always 3 ints after .convert('RGB')
                r, g, b = cast(Tuple[int, int, int], img.getpixel((x, y)))

                # Clear the last bit of red, then set it to our secret bit
                # e.g. if red = 200 (11001000) and bit = 1 → 201 (11001001)
                new_r = (r & ~1) | int(binary_message[bit_index])

                img.putpixel((x, y), (new_r, g, b))
                bit_index += 1

    # Save the modified image to memory and send it back
    output = io.BytesIO()
    img.save(output, 'PNG')
    output.seek(0)

    return send_file(output, mimetype='image/png', as_attachment=True, download_name='secret_image.png')


# ── Route: Read a hidden message from an image ────────────────────────────────
@app.route('/api/reveal', methods=['POST'])
def reveal_text():
    image_file = request.files['image']
    img = Image.open(image_file.stream).convert('RGB')
    width, height = img.size

    extracted_bits = ""

    # Read the last bit of each pixel's red value
    for y in range(height):
        for x in range(width):
            r, g, b = cast(Tuple[int, int, int], img.getpixel((x, y)))
            extracted_bits += str(r & 1)  # last bit is either 0 or 1

    # Convert all those bits back into text
    full_text = binary_to_text(extracted_bits)

    # Look for our stop marker #####
    if "#####" in full_text:
        message = full_text.split("#####")[0]
        return jsonify({'message': message})

    return jsonify({'error': 'No hidden message found in this image'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)