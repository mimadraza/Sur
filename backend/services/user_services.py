from backend.db.queries import call_procedure, get_random_songs, get_random_albums, get_song_by_id, create_song, create_album, search_songs_by_name, search_albums_by_name, search_artists_by_name


def follow_artist(user_id, artist_id):
    params = [user_id, artist_id]
    call_procedure('follow_artist', params)

def get_home_page_data():
    # Fetch random songs and albums
    songs = get_random_songs()
    albums = get_random_albums()

    # Initialize lists to store the song metadata and file data
    random_song_data = []
    album_song_data = []

    # Add random songs and their files
    for song in songs:
        song_id = song['song_id']  # Assuming the song dictionary has an 'id'
        song_file = get_song_metadata_and_file(song_id)
        random_song_data.append(song_file)

    # Add album songs and their files
    for album in albums:
        album_data = []  # This will hold the songs in the album
        for album in album['album_id']:  # Assuming album has a 'songs' key with a list of songs
            song_id = song['song_id']
            song_file = get_song_metadata_and_file(song_id)
            album_data.append(song_file)
        album_song_data.append(album_data)  # Add the list of songs for this album to album_song_data

    print(songs)

    # Return both random songs and album songs in separate lists
    return {
        "songs": random_song_data,  # 1D list of random songs
        "albums": album_song_data   # 2D list of songs within albums
    }

def get_song_metadata_and_file(song_id):
    song = get_song_by_id(song_id)
    if not song:
        print(404)
        return {"message": "Song not found"}, 404
    file_name = f"{song_id}.mp3"
    return {"metadata": song, "file_name": file_name , "song_id": song_id}


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