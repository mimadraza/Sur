from flask import Flask, jsonify, make_response, send_file, request
from flask_cors import CORS
from routes import auth_blueprint
from routes import user_blueprint

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = '4.145.91.69'
app.config['MYSQL_USER'] = 'admin1'
app.config['MYSQL_PASSWORD'] = 'P@ssword123'
app.config['MYSQL_DB'] = 'SUR'

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/user')
@app.route('/')
def hello_world():
    return make_response({"message": "Hello, Saad!"})

# @app.route('/get_music/<song_name>', methods=['GET'])
# def get_music(song_name):
#     # Assuming the song name is used to get the file path from a database
#     song_path = 'musics/Song 1.mp3'
#
#     # Return the file path to the frontend
#     return send_file(song_path, mimetype='audio/mpeg')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
