from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/foo')
def foo():
    test = 'asdfasdf'
    return render_template('foo.html', content=test)

if __name__ == "__main__":
    app.run(debug=True)