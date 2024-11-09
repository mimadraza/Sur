from flask import Flask, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return make_response({"message": "Hello, Saad!"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
