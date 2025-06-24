from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/information')
def information():
    return render_template('information.html')

if __name__ == '__main__':
    app.run(debug=True)