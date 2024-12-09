import datetime

from backend.db.queries import call_procedure, get_random_songs, get_random_albums, get_song_by_id, create_song, \
    create_album, search_songs_by_name, search_albums_by_name, search_artists_by_name, get_songs_by_album_id


def follow_artist(user_id, artist_id):
    params = [user_id, artist_id]
    call_procedure('follow_artist', params)


def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime objects to ISO format string
    raise TypeError(f"Type {type(obj)} not serializable")

def get_home_page_data():
    # Fetch random songs and albums
    songs = get_random_songs()
    albums = get_random_albums()

    random_song_data = []
    album_song_data = []

    # Add random songs and their titles/song_ids
    for song in songs:
        song_id = song['song_id']  # Assuming the song dictionary has an 'id'
        song_file = get_song_metadata_and_file(song_id)
        
        # Directly extract 'song_id' and 'title' from the song metadata
        random_song_data.append({
            'song_id': song_file['metadata']['song_id'],
            'title': song_file['metadata']['title']
        })

    # Add album songs and their titles/song_ids
    for album in albums:
        album_data = []  # This will hold the songs in the album

        # Fetch songs associated with the album
        album_songs = get_songs_by_album_id(album['album_id'])  # Replace with actual function

        for song in album_songs:
            song_id = song['song_id']
            song_file = get_song_metadata_and_file(song_id)
            
            # Directly extract 'song_id' and 'title' from the song metadata
            album_data.append({
                'song_id': song_file['metadata']['song_id'],
                'title': song_file['metadata']['title']
            })

        album_song_data.append(album_data)

    # Return the final data
    return {
        "songs": random_song_data,  # 1D list of random songs with 'song_id' and 'title'
        "albums": album_song_data  # 2D list of songs within albums, each having 'song_id' and 'title'
    }

def get_song_metadata_and_file(song_id):
    song = get_song_by_id(song_id)
    if not song:
        print(404)
        return {"message": "Song not found"}, 404

    # Convert release_date to string if it's a datetime object
    release_date = song['release_date']
    if isinstance(release_date, datetime):  # Correctly check if release_date is a datetime object
        release_date = release_date.isoformat()  # Convert to ISO string

    song_metadata = {
        'song_id': song['song_id'],
        'title': song['title'],
        # 'duration': song['duration'],
        # 'release_date': release_date,  # Now it is a string if it was datetime
        # # Add any other fields you need that are simple types
    }

    file_name = f"{song_id}.mp3"
    return {"metadata": song_metadata, "file_name": file_name}


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