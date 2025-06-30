# image_processing_app.py (Backend - Flask)
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from PIL import Image, ImageFilter

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return redirect(url_for('process_image', filename=filename))
    return render_template('upload.html')

@app.route('/process/<filename>', methods=['GET', 'POST'])
def process_image(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], filename)

    if request.method == 'POST':
        filter_type = request.form['filter']
        try:
            img = Image.open(filepath)
            if filter_type == 'blur':
                processed_img = img.filter(ImageFilter.BLUR)
            elif filter_type == 'contour':
                processed_img = img.filter(ImageFilter.CONTOUR)
            elif filter_type == 'edge_enhance':
                processed_img = img.filter(ImageFilter.EDGE_ENHANCE)
            elif filter_type == 'grayscale':
                processed_img = img.convert("L")
            else:
                processed_img = img #no change.
            processed_img.save(processed_filepath)
            return render_template('processed.html', original_filename=filename, processed_filename=filename)

        except Exception as e:
            return f"Error processing image: {e}"

    return render_template('process.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)