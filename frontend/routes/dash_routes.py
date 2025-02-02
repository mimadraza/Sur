from flask import Blueprint, request, redirect, render_template, jsonify
from frontend.services import dash_services

userdash_blueprint = Blueprint('userdash', __name__)
artistdash_blueprint = Blueprint('artistdash', __name__)

@userdash_blueprint.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    user_data = dash_services.user_dashboard()
    if user_data.status_code == 200:
        data = user_data.json()
        albums = data['albums']
        songs = data['songs']
        return render_template('userdashboard.html', albums=albums, songs=songs)
    return render_template('userdashboard.html', artist_data = user_data)

@artistdash_blueprint.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    user_data = dash_services.artist_dashboard()
    print(user_data)
    
    return render_template('artistdashboard.html', artist_data = user_data)

@artistdash_blueprint.route('/stats', methods = ['GET', 'POST'])
def stats():
    user_data = dash_services.stats()

    return render_template('Analytics.html', artist_data = user_data)

@artistdash_blueprint.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        dash_services.upload(request)
    else:
        return render_template('upload.html')

@artistdash_blueprint.route('/album', methods = ['GET', 'POST'])
def album():
    artist_album = dash_services.album()
    return render_template('artistalbum.html', artist_data = artist_album)

@userdash_blueprint.route('/album/<album_id>', methods=['GET', 'POST'])
def album():
    # Get the album name from the URL query parameters
    user_data = dash_services.user_album()
    out = None
    if user_data.status_code == 200:
        data = user_data.json()
        albums = data['albums']
    # Loop through the albums and find the one matching the album_id
    for album in albums:
        if album['title'] == album_id:
                out = album
    
    # If no album is found, you can handle this scenario here
    if not out:
        return "Album not found", 404
    
    # Pass the album data to the template
    return render_template('albums.html', album=out)


@userdash_blueprint.route('/search', methods = ['POST'])
def search():
    result = dash_services.search(request.form['search'])
    return render_template('searchpage.html', artist_data = result)
@artistdash_blueprint.route('/search', methods = ['POST'])
def search():
    result = dash_services.search(request.form['search'])
    return render_template('searchpage.html', artist_data = result)

@userdash_blueprint.route("/playlist", methods=["POST"])
def create_playlist():
    # Get the token from cookies
    token = request.cookies.get('token')

    if not token:
        return jsonify({"error": "Authentication required"}), 401

    # Decode the token to get the user ID
    user_id = get_user_from_token(token)

    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Get the data from the request
    data = request.json
    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return jsonify({"error": "Playlist title is required"}), 400

    # Create the playlist
    playlist_id = create_new_playlist(user_id, title, description)
    return jsonify({"message": "Playlist created successfully", "playlist_id": playlist_id}), 201

# Add song to playlist
@userdash_blueprint.route("/playlist/<int:playlist_id>/song/<int:song_id>", methods=["POST"])
def add_song_to_playlist_route(playlist_id, song_id):
    # Get the token from cookies
    token = request.cookies.get('token')

    if not token:
        return jsonify({"error": "Authentication required"}), 401

    # Decode the token to get the user ID
    user_id = get_user_from_token(token)

    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Add the song to the playlist
    add_song_to_playlist(playlist_id, song_id)
    return jsonify({"message": "Song added to playlist successfully"}), 200

# Remove song from playlist
@userdash_blueprint.route("/playlist/<int:playlist_id>/song/<int:song_id>", methods=["DELETE"])
def remove_song_from_playlist_route(playlist_id, song_id):
    # Get the token from cookies
    token = request.cookies.get('token')

    if not token:
        return jsonify({"error": "Authentication required"}), 401

    # Decode the token to get the user ID
    user_id = get_user_from_token(token)

    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Remove the song from the playlist
    remove_song_from_playlist(playlist_id, song_id)
    return jsonify({"message": "Song removed from playlist successfully"}), 200

# Get all playlists for a user
@userdash_blueprint.route("/playlists", methods=["GET"])
def get_playlists():
    # Get the token from cookies
    token = request.cookies.get('token')

    if not token:
        return jsonify({"error": "Authentication required"}), 401

    # Decode the token to get the user ID
    user_id = get_user_from_token(token)

    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Fetch all playlists for the user
    playlists = get_playlists_for_user(user_id)
    return jsonify({"playlists": playlists}), 200

# Get all songs in a specific playlist
@userdash_blueprint.route("/playlist/<int:playlist_id>/songs", methods=["GET"])
def get_songs_in_playlist_route(playlist_id):
    # Get the token from cookies
    token = request.cookies.get('token')

    if not token:
        return jsonify({"error": "Authentication required"}), 401

    # Decode the token to get the user ID
    user_id = get_user_from_token(token)

    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Fetch all songs in the playlist
    songs = get_songs_in_playlist(playlist_id)
    return jsonify({"songs": songs}), 200