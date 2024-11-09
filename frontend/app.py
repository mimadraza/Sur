import requests
from flask import Flask
from config import Config

app = Flask(__name__)
backendurl = Config.BACKEND_URL


@app.route('/')
def hello_world():
    response = requests.get(backendurl)
    return response.text


if __name__ == '__main__':
    app.run(debug=True, port=5001)
