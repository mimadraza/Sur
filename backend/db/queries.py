from backend.db.db_connection import get_db_connection

def get_user_by_email(email):
    print("reached query function")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def call_procedure(proc_name, params):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.callproc(proc_name, params)
        else:
            cursor.callproc(proc_name)
        connection.commit()
        # Fetch results if the procedure returns data
        results = []
        for result in cursor.stored_results():
            results = result.fetchall()

        return results
    finally:
        cursor.close()
        connection.close()

def get_random_songs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Song ORDER BY RAND() LIMIT 5")
    songs = cursor.fetchall()
    cursor.close()
    conn.close()
    return songs

def get_random_songs_for_artist(artist_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Song ORDER BY RAND() LIMIT 5 WHERE artist_id = %s", (artist_id,))
    songs = cursor.fetchall()
    cursor.close()
    conn.close()
    return songs

def get_song_by_id(song_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Song WHERE song_id = %s", (song_id,))
    song = cursor.fetchone()
    cursor.close()
    conn.close()
    return song

def create_song(title, duration, release_date, album_id, genre_id, artist_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Song (title, duration, release_date, album_id, genre_id, artist_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (title, duration, release_date, album_id, genre_id, artist_id))
    song_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return song_id

def get_songs_by_album_id(album_id):
    # Assuming you have a function that retrieves all songs for a given album ID
    # This function would query your database and return a list of songs for the given album
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Song WHERE album_id = %s", (album_id,))
    songs = cursor.fetchall()
    cursor.close()
    conn.close()
    return songs

# Albums
def get_random_albums():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Album ORDER BY RAND() LIMIT 5")
    albums = cursor.fetchall()
    cursor.close()
    conn.close()
    return albums

def get_random_albums_for_artist(artist_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Album ORDER BY RAND() LIMIT 5 WHERE artist_id = %s", (artist_id,))
    albums = cursor.fetchall()
    cursor.close()
    conn.close()
    return albums

def create_album(title, genre_id, artist_id, album_type, release_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Album (title, genre_id, artist_id, album_type, release_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, genre_id, artist_id, album_type, release_date))
    album_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return album_id

def search_songs_by_name(name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT * FROM Song
        WHERE title LIKE %s
    """
    cursor.execute(query, ('%' + name + '%',))
    songs = cursor.fetchall()
    cursor.close()
    conn.close()
    return songs

def search_albums_by_name(name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT * FROM Album
        WHERE title LIKE %s
    """
    cursor.execute(query, ('%' + name + '%',))
    albums = cursor.fetchall()
    cursor.close()
    conn.close()
    return albums

def search_artists_by_name(name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT *
        FROM Artist
        WHERE CONCAT(first_name, ' ', last_name) LIKE %s
    """
    cursor.execute(query, ('%' + name + '%',))
    artists = cursor.fetchall()
    cursor.close()
    conn.close()
    return artists


# Fetch artist by email (for login)
def get_artist_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Artist WHERE email = %s", (email,))
    artist = cursor.fetchone()
    cursor.close()
    conn.close()
    return artist

# Insert a new artist (for registration)
def create_artist(first_name, last_name, email, password_hash, date_of_birth, bio, country):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Artist (first_name, last_name, email, password_hash, date_of_birth, bio, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (first_name, last_name, email, password_hash, date_of_birth, bio, country))
    artist_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return artist_id

# Create a new playlist
def create_playlist(user_id, title, description=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Playlist (title, description, user_id)
        VALUES (%s, %s, %s)
    """, (title, description, user_id))
    playlist_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return playlist_id

# Add a song to a playlist
def add_song_to_playlist(playlist_id, song_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Playlist_Song (playlist_id, song_id)
        VALUES (%s, %s)
    """, (playlist_id, song_id))
    conn.commit()
    cursor.close()
    conn.close()

# Remove a song from a playlist
def remove_song_from_playlist(playlist_id, song_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM Playlist_Song
        WHERE playlist_id = %s AND song_id = %s
    """, (playlist_id, song_id))
    conn.commit()
    cursor.close()
    conn.close()

# Get all playlists for a user
def get_playlists_for_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Playlist WHERE user_id = %s", (user_id,))
    playlists = cursor.fetchall()
    cursor.close()
    conn.close()
    return playlists

# Get all songs in a specific playlist
def get_songs_in_playlist(playlist_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.song_id, s.title, s.duration, s.release_date, s.album_id, s.genre_id, s.artist_id, s.playbacks
        FROM Playlist_Song ps
        JOIN Song s ON ps.song_id = s.song_id
        WHERE ps.playlist_id = %s
    """, (playlist_id,))
    songs = cursor.fetchall()
    cursor.close()
    conn.close()
    return songs
