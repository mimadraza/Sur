from flask import Flask, request, render_template
from config import Config
# import CORS

app = Flask(__name__, static_folder='static')
# CORS(app)
backendurl = Config.BACKEND_URL


@app.route('/')
def index():  # put application's code here
    return render_template('LoginPage.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
