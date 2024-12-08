from flask import app, jsonify, request


@app.route('/get-songs', methods=['GET'])
def get_songs():
    query = request.args.get('query', '').lower()
    
    # Dummy list of songs (replace this with a database query)
    all_songs = [
        {'id': 1, 'title': 'Song One'},
        {'id': 2, 'title': 'Song Two'},
        {'id': 3, 'title': 'Song Three'},
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
