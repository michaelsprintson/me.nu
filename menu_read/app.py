import os
import json
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
import reviewparse
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['POST', 'GET'])
def index():
    did_update = False
    submission_message = "Preferences saved!"
    if request.method == 'POST':
        if request.form['budget'].isdigit():
            json.dump(request.form, open('preferencesData.json', 'w'))
        else:
            submission_message = "Invalid input, please try again"
        did_update = True
    # Load user preferences
    user_preferences = json.load(open('preferencesData.json'))
    return render_template('index.html', user_preferences=user_preferences, did_update=did_update, submission_message=submission_message)


@app.route('/chooseMenu')
def choose_menu():
    return render_template('chooseMenu.html')


@app.route('/takePicMala/<pic_error>')
def take_pic_mala(pic_error):
    text_file = open("foodChoice.txt", "w")
    text_file.write("True")
    text_file.close()
    return render_template('takePic.html', pic_error=pic_error)


@app.route('/takePicSharetea/<pic_error>')
def take_pic_sharetea(pic_error):
    text_file = open("foodChoice.txt", "w")
    text_file.write("False")
    text_file.close()
    return render_template('takePic.html', pic_error=pic_error)


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
    foodChoice = open("foodChoice.txt", "r")
    food = foodChoice.readline() in ['True']

    # Get image
    pic_loc = 'static/webcam.jpg'

    # Get preferences
    pref = "preferencesData.json"

    if food:
        menu_data = json.load(open('rankingMala.json'))
    else:
        menu_data = json.load(open('rankingSharetea.json'))
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
    # Analyze menu, catch OCR error
    try:
        reviewparse.overall(food, pic_loc, pref)
        # Filter top results
        menu_data = json.load(open('ranking.json'))
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
    except:
        if food:
            # Mala
            return redirect(url_for('take_pic_mala', pic_error=True))
        # Sharetea
        return redirect(url_for('take_pic_sharetea', pic_error=True))


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0')
