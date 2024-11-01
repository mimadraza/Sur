from flask import Flask
from config import Config
import CORS

app = Flask(__name__)
CORS(app)
backendurl = Config.BACKEND_URL


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, port=5001)
