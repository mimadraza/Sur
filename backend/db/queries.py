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

# Albums
def get_random_albums():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Album ORDER BY RAND() LIMIT 5")
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
        SELECT song_id, song_name FROM songs
        WHERE song_name LIKE %s
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
        SELECT album_id, album_name FROM albums
        WHERE album_name LIKE %s
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
        SELECT artist_id, artist_name FROM artists
        WHERE artist_name LIKE %s
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