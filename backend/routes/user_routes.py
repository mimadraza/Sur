from flask import Blueprint, request, jsonify, send_from_directory
from backend.services.user_services import get_home_page_data, get_song_metadata_and_file, upload_song, upload_album, \
    search_songs_albums_artists, get_home_page_data_for_artist
import json
from flask import Blueprint, request, jsonify
from backend.services.user_services import create_new_playlist, add_song_to_playlist, remove_song_from_playlist, \
    get_playlists_for_user, get_songs_in_playlist
from backend.utils.tokens import get_user_from_token

user_blueprint = Blueprint('user', __name__)
artist_blueprint = Blueprint('artist', __name__)

@artist_blueprint.route("/home/", methods=["GET"])
def home_page():
    # Get the token from cookies
    token = request.cookies.get('token')

    if not token:
        return jsonify({"error": "Authentication required"}), 401

    # Decode the token to get the user ID
    user_id = get_user_from_token(token)

    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Use the user_id to get the artist or user-specific data
    data = get_home_page_data_for_artist(user_id)  # Fetch data using user_id

    # Try serializing the data before passing it to jsonify
    try:
        # Attempt to convert the data to a JSON string to check if it's serializable
        json.dumps(data)
    except (TypeError, ValueError) as e:
        # If serialization fails, return an error response with a 400 status code
        return jsonify({"error": "Data is not serializable", "message": str(e)}), 400

    # If data is serializable, return it as a JSON response
    return jsonify(data), 200

@user_blueprint.route("/home", methods=["GET"])
def home_page():
    data = get_home_page_data()

    # Try serializing the data before passing it to jsonify
    try:
        # Attempt to convert the data to a JSON string to check if it's serializable
        json.dumps(data)
    except (TypeError, ValueError) as e:
        # If serialization fails, return an error response with a 400 status code
        return jsonify({"error": "Data is not serializable", "message": str(e)}), 400

    # If data is serializable, return it as a JSON response
    return jsonify(data), 200

@user_blueprint.route("/song/<int:song_id>", methods=["GET"])
def get_song(song_id):
    song_data = get_song_metadata_and_file(song_id)
    return jsonify(song_data), 200

@user_blueprint.route("/upload/song", methods=["POST"])
def upload_new_song():
    data = request.json
    song_id = upload_song(**data)
    return jsonify({"message": "Song uploaded successfully", "song_id": song_id}), 201

@user_blueprint.route("/upload/album", methods=["POST"])
def upload_new_album():
    data = request.json
    album_id = upload_album(**data)
    return jsonify({"message": "Album uploaded successfully", "album_id": album_id}), 201

@user_blueprint.route("/search", methods=["POST"])
def search():
    data = request.json
    query = data["search"]
    if not query:
        return jsonify({"message": "Query parameter is required"}), 400

    search_results = search_songs_albums_artists(query)
    return jsonify(search_results), 200

@user_blueprint.route("/song/<int:song_id>/file", methods=["GET"])
def get_song_file(song_id):
    song_metadata = get_song_metadata_and_file(song_id)

    # Check if song_metadata contains the file_name
    if "file_name" in song_metadata:
        file_name = song_metadata["file_name"]
        if file_name:
            return send_from_directory("D:\Songs", file_name), 200
        else:
            return jsonify({"message": "Song file not found"}), 404
    else:
        # In case the song was not found or another issue
        return song_metadata

# Create a new playlist
@user_blueprint.route("/playlist", methods=["POST"])
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
@user_blueprint.route("/playlist/<int:playlist_id>/song/<int:song_id>", methods=["POST"])
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
@user_blueprint.route("/playlist/<int:playlist_id>/song/<int:song_id>", methods=["DELETE"])
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
@user_blueprint.route("/playlists", methods=["GET"])
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
@user_blueprint.route("/playlist/<int:playlist_id>/songs", methods=["GET"])
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
