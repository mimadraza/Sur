import datetime

from backend.db.queries import call_procedure, get_random_songs, get_random_albums, get_song_by_id, create_song, \
    create_album, search_songs_by_name, search_albums_by_name, search_artists_by_name, get_songs_by_album_id, \
    get_random_albums_for_artist, get_random_songs_for_artist


def serialize_song(song):
    return {
        "song_id": song["song_id"],
        "title": song["title"],
        "duration": str(song["duration"]),  # Convert TIME to string format
        "release_date": song["release_date"].strftime('%Y-%m-%d') if song["release_date"] else None,
        "album_id": song["album_id"],
        "genre_id": song["genre_id"],
        "artist_id": song["artist_id"],
        "playbacks": song["playbacks"]
    }

# Helper function to serialize album data
def serialize_album(album, songs):
    return {
        "album_id": album["album_id"],
        "title": album["title"],
        "album_type": album["album_type"],
        "release_date": album["release_date"].strftime('%Y-%m-%d') if album["release_date"] else None,
        "songs": songs  # List of songs for this album
    }

def follow_artist(user_id, artist_id):
    params = [user_id, artist_id]
    call_procedure('follow_artist', params)

def get_home_page_data_for_artist(artist_id):
    # Fetch random songs and albums
    albums = get_random_albums_for_artist(artist_id)

    all_albums_data = []

    for album in albums:
        album_id = album["album_id"]

        # Fetch songs for the current album
        songs = get_songs_by_album_id(album_id)

        # Serialize songs
        serialized_songs = [serialize_song(song) for song in songs]

        # Serialize album data along with its songs
        serialized_album = serialize_album(album, serialized_songs)
        all_albums_data.append(serialized_album)

    songs = get_random_songs_for_artist(artist_id)
    serialized_songs = [serialize_song(song) for song in songs]

    return {
        "albums": all_albums_data,  # 5 random albums with their songs
        "songs": serialized_songs  # 5 random songs (independently)
    }

def get_home_page_data():
    # Fetch random songs and albums
    albums = get_random_albums()

    all_albums_data = []

    for album in albums:
        album_id = album["album_id"]

        # Fetch songs for the current album
        songs = get_songs_by_album_id(album_id)

        # Serialize songs
        serialized_songs = [serialize_song(song) for song in songs]

        # Serialize album data along with its songs
        serialized_album = serialize_album(album, serialized_songs)
        all_albums_data.append(serialized_album)

    songs = get_random_songs()
    serialized_songs = [serialize_song(song) for song in songs]

    return {
        "albums": all_albums_data,  # 5 random albums with their songs
        "songs": serialized_songs  # 5 random songs (independently)
    }

    # random_song_data = []
    # album_song_data = []
    #
    # # Add random songs and their files
    # for song in songs:
    #     song_id = song['song_id']  # Assuming the song dictionary has an 'id'
    #     song_file = get_song_metadata_and_file(song_id)
    #     if isinstance(song_file, dict):
    #         random_song_data.append(song_file)
    #
    # # Add album songs and their files
    # for album in albums:
    #     album_data = []  # This will hold the songs in the album
    #
    #     # Fetch songs associated with the album
    #     album_songs = get_songs_by_album_id(album['album_id'])  # Replace with actual function
    #
    #     for song in album_songs:
    #         song_id = song['song_id']
    #         song_file = get_song_metadata_and_file(song_id)
    #         if isinstance(song_file, dict):
    #             album_data.append(song_file)
    #
    #     album_song_data.append(album_data)

    # Return the final data (ensure all objects are serializable)
    # return {
    #     "songs": songs,  # 1D list of random songs
    #     "albums": albums  # 2D list of songs within albums
    # }

def get_song_metadata_and_file(song_id):
    song = get_song_by_id(song_id)
    if not song:
        print(404)
        return {"message": "Song not found"}, 404
    file_name = f"{song_id}.mp3"
    return {"metadata": song, "file_name": file_name}


def upload_song(title, duration, release_date, album_id, genre_id, artist_id):
    song_id = create_song(title, duration, release_date, album_id, genre_id, artist_id)
    return song_id

def upload_album(title, genre_id, artist_id, album_type, release_date):
    album_id = create_album(title, genre_id, artist_id, album_type, release_date)
    return album_id

def search_songs_albums_artists(query):
    # Search for songs, albums, and artists that match the query
    song_results = search_songs_by_name(query)
    album_results = search_albums_by_name(query)
    artist_results = search_artists_by_name(query)

    # Combine the results into a single dictionary
    results = {
        "songs": song_results,
        "albums": album_results,
        "artists": artist_results
    }

    return results