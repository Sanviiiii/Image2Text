from flask import Flask, request, render_template, url_for
from PIL import Image, UnidentifiedImageError
import pytesseract
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if necessary

history = []

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    extracted_text = None
    image_url = None
    if request.method == 'POST':
        file = request.files['file']
        lang = request.form['lang']
        try:
            image = Image.open(file)
            text = pytesseract.image_to_string(image, lang=lang)
            extracted_text = text
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            image.save(image_path)
            image_url = url_for('static', filename=f'uploads/{file.filename}')
            history.append({'image_path': f'uploads/{file.filename}', 'text': text})
            if len(history) > 5:
                history.pop(0)
        except UnidentifiedImageError:
            return "The file is not a valid image."
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('index.html', extracted_text=extracted_text, image_url=image_url, history=history)

if __name__ == '__main__':
    app.run(debug=True)
