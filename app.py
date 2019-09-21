import os
from flask import Flask, flash, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def upload():
    return render_template("index.html")


@app.route('/foo', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return render_template("foo.html", name=f.filename)


@app.route('/foo')
def foo():
    test = 'asdfasdf'
    return render_template('foo.html', content=test)


if __name__ == "__main__":
    app.run(debug=True)