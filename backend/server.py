from flask import Flask, jsonify, make_response, send_file, request
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from routes.auth_routes import auth_blueprint
from routes.user_routes import user_blueprint



app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/user')
@app.route('/')
def hello_world():
    return make_response({"message": "Hello, Saad!"})

# @app.route('/get_music/<song_name>', methods=['GET'])
# def get_music(song_name):
#     # Assuming the song name is used to get the file path from a database
#     song_path = 'musics/Song 1.mp3'

#     # Return the file path to the frontend
#     return send_file(song_path, mimetype='audio/mpeg')
@app.route('/get-songs', methods=['GET'])
def get_songs():
    query = request.args.get('query', '').lower()
    
    # Dummy list of songs (replace this with a database query)
    all_songs = [
        {'id': 1, 'title': 'Song 1'},
        {'id': 2, 'title': 'Song 2'},
        {'id': 3, 'title': 'Song 3'},
        {'id': 4, 'title': 'Another Song'},
        {'id': 5, 'title': 'Final Song'},
    ]
    
    # Filter songs based on the query
    filtered_songs = [song for song in all_songs if query in song['title'].lower()]
    return jsonify({'songs': filtered_songs})
@app.route('/create-playlist', methods=['POST'])
def create_playlist():
    data = request.get_json()
    playlist_name = data.get('playlistName')
    song_ids = data.get('songIds')

    # Log or store the playlist
    print(f"New Playlist Created: {playlist_name}")
    print(f"Song IDs: {song_ids}")
    
    # Return success message
    return jsonify({'message': f'Playlist "{playlist_name}" created successfully!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
