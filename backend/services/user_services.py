from backend.db.queries import call_procedure, get_random_songs, get_random_albums, get_song_by_id, create_song, create_album, search_songs_by_name, search_albums_by_name, search_artists_by_name


def follow_artist(user_id, artist_id):
    params = [user_id, artist_id]
    call_procedure('follow_artist', params)

def get_home_page_data():
    songs = get_random_songs()
    albums = get_random_albums()
    return {"songs": songs, "albums": albums}

def get_song_metadata_and_file(song_id):
    song = get_song_by_id(song_id)
    if not song:
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