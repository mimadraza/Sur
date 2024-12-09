from flask import Blueprint, request, jsonify, send_from_directory
from backend.services.user_services import get_home_page_data, get_song_metadata_and_file, upload_song, upload_album, \
    search_songs_albums_artists, get_home_page_data_for_artist
import json
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
            return send_from_directory("E:\Songs", file_name), 200
        else:
            return jsonify({"message": "Song file not found"}), 404
    else:
        # In case the song was not found or another issue
        return song_metadata