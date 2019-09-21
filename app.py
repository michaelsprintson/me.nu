import os
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chooseMenu')
def choose_menu():
    return render_template('chooseMenu.html')


@app.route('/takePic')
def take_pic():
    return render_template('takePic.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/saveImage', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'webcam' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['webcam']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=webcam>
      <input type=submit value=Upload>
    </form>
    # '''


@app.route('/loading')
def loading():
    return render_template('loading.html')


@app.route('/suggestedMenu')
def suggested_menu():
    return render_template('suggestedMenu.html')


@app.route('/foo')
def foo():
    test = 'asdfasdf'
    return render_template('foo.html', content=test)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True)