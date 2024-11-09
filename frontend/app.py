import requests
from flask import Flask
from config import Config

app = Flask(__name__)
backendurl = Config.BACKEND_URL


@app.route('/')
def index():  # put application's code here
    return render_template('LoginPage.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
