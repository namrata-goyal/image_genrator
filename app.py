from flask import Flask, render_template, url_for
from PIL import Image
import requests
import io
import os

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image/<category>')
def generate_image(category):
    if category == "Print Designs":
        query = " printable sticker"
    elif category == "Dresses":
        query = "dress"
    elif category == "Sticker Collection":
        query = "asthetic sticker"
    else:
        query = "fashion"

    url = f"https://api.unsplash.com/photos/random?query={query}&orientation=landscape&client_id=1LTkhTUnZrPDHd0WX_9Jmp0ZoXjYQ8YX8lQbYxKiR90"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        img_response = requests.get(data["urls"]["regular"])
        if img_response.status_code == 200:
            img_data = img_response.content
            original_image = Image.open(io.BytesIO(img_data)).resize((600, 400), resample=Image.LANCZOS)

            # Ensure the static directory exists
            static_dir = 'static'
            if not os.path.exists(static_dir):
                os.makedirs(static_dir)

            # Save the image to the static folder
            image_path = os.path.join(static_dir, f'{category}.jpg')
            original_image.save(image_path)

            return render_template('image.html', image_url=url_for('static', filename=f'{category}.jpg'))
        else:
            return f"Failed to retrieve image from Unsplash: {img_response.status_code}", 500
    else:
        return f"Failed to get data from Unsplash API: {response.status_code}", 500

if __name__ == '__main__':
    app.run()
