from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import io
import os
import base64

app = Flask(__name__, template_folder='templates')

def image_to_data_uri(image, format='JPEG'):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format)
    img_byte_arr.seek(0)
    data_uri = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    return f"data:image/{format.lower()};base64,{data_uri}"

def pixelate(image_file, pixel_size):
    image = Image.open(image_file)
    width, height = image.size
    new_width = max(1, width // pixel_size)
    new_height = max(1, height // pixel_size)

    image_small = image.resize((new_width, new_height), resample=Image.NEAREST)
    result = image_small.resize((width, height), Image.NEAREST)

    original_data_uri = image_to_data_uri(image)
    pixelated_data_uri = image_to_data_uri(result)

    return original_data_uri, pixelated_data_uri

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        pixel_size = int(request.form.get('pixel_size', 16))  # Default pixel size is 16
        if file and file.filename:
            original_img, pixelated_img = pixelate(file, pixel_size)
            return render_template('display_image.html', original_image=original_img, pixelated_image=pixelated_img)
    return render_template('upload_form.html')

if __name__ == '__main__':
    app.run(debug=True)