from flask import Flask, request, render_template, redirect, url_for, flash
from PIL import Image
import pytesseract
import os
from pdf2image import convert_from_path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'supersecretkey'

# Update this path to the location of the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
languages='hin'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        text = ""
        if file.filename.lower().endswith('.pdf'):
            # Convert PDF to images
            images = convert_from_path(filepath)
            for image in images:
                text += pytesseract.image_to_string(image,languages)
        else:
            # Open the image file and extract text
            try:
                image = Image.open(filepath)
                text = pytesseract.image_to_string(image)
            except PIL.UnidentifiedImageError:
                flash('Cannot identify image file')
                return redirect(request.url)
        
        return render_template('index.html', extracted_text=text, image_url=filepath if not file.filename.lower().endswith('.pdf') else None)
    else:
        flash('Allowed file types are png, jpg, jpeg, gif, pdf')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
