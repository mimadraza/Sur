from flask import Blueprint, request, jsonify, send_from_directory
from backend.services.user_services import get_home_page_data, get_song_metadata_and_file, upload_song, upload_album, search_songs_albums_artists

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route("/home", methods=["GET"])
def home_page():
    data = get_home_page_data()
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

@user_blueprint.route("/search", methods=["GET"])
def search():
    query = request.args.get('query')
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