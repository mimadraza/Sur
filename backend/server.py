from flask import Flask, jsonify, make_response, send_file
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return make_response({"message": "Hello, Saad!"})

@app.route('/get_music/<song_name>', methods=['GET'])
def get_music(song_name):
    # Assuming the song name is used to get the file path from a database
    song_path = 'musics/Song 1.mp3'

    # Return the file path to the frontend
    return send_file(song_path, mimetype='audio/mpeg')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
