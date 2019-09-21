from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/foo')
def foo():
    test = 'asdfasdf'
    return render_template('foo.html', content=test)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return jsonify(request.form['userID'], request.form['file'])
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)