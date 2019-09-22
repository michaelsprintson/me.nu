import os
import json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
import menu_read.reviewparse as rp
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['budget'].isdigit():
            json.dump(request.form, open('menu_read/preferencesData.json', 'w'))
    return render_template('index.html')


@app.route('/chooseMenu')
def choose_menu():
    return render_template('chooseMenu.html')


@app.route('/takePicMala')
def take_pic_mala():
    text_file = open("menu_read/foodChoice.txt", "w")
    text_file.write("True")
    text_file.close()
    return render_template('takePic.html')


@app.route('/takePicSharetea')
def take_pic_sharetea():
    text_file = open("menu_read/foodChoice.txt", "w")
    text_file.write("False")
    text_file.close()
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
    # Get food T/F
    foodChoice = open("menu_read/foodChoice.txt", "r")
    food = foodChoice.readline() in ['True']

    # Get image
    pic_loc = 'static/webcam.jpg'

    # Get preferences
    pref = "menu_read/preferencesData.json"

    # Analyze menu
    rp.overall(food, pic_loc, pref)

    # Filter top results
    menu_data = json.load(open('menu_read/ranking.json'))
    top_items = []
    other_items = []
    i = 0
    for menu_item in menu_data:
        if i < 3:
            top_items.append(menu_item)
        elif len(other_items) < 7:
            other_items.append(menu_item)
        i += 1
    return render_template('suggestedMenu.html', topItems=top_items, otherItems=other_items, menuData=menu_data)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    port = int(os.environ.get("PORT", 8080))
    #host='0,0,0,0',port=port
    app.run(debug=True, host='0,0,0,0', port=port)