import requests
from flask import current_app

# Access the backend URL
def get_backend_url():
    # Access the configuration when needed
    return current_app.config['BACKEND_URL']

#artist data and user_data should be globally declared
artist_data = {
        'background_url': '../static/images/artistbackground.jpg',
        'profile_url': '../static/images/Hozier.webp',
        'Artist_rank': 12,
        'Artist_Followers': 100,
        'Artist_likes': 100,
        'songs': [
            {'title': 'Too Sweet', 'image_url': '../static/images/images.jpg' , 'percent': '40'},
            {'title': 'Sweet Melody', 'image_url': '../static/images/dinner.jpg', 'percent': '100'},
            {'title': 'Angel of Sweet death and Codiene Scene', 'image_url': '../static/images/angel.jpg', 'percent': '60'},
            {'title': 'Take me to Church', 'image_url': '../static/images/church.jpg', 'percent': '70'},
            {'title': 'Dinner', 'image_url': '../static/images/church.jpg', 'percent': '50'}
        ],
        'albums' : [
        {'title': 'Unreal Unearth', 'image_url': '../static/images/Church.jpg'},
        {'title': 'Future Nostalgia', 'image_url': '../static/images/dinner.jpg'},
        {'title': 'After Hours', 'image_url': '../static/images/angel.jpg'},
        {'title': 'Wasteland Baby!', 'image_url': '../static/images/image.jpg'},
        {'title': 'After Hours', 'image_url': '../static/images/after_hours.jpg'}
        ]
}


user_data = {
        'songs': [
            {'title': 'Too Sweet', 'image_url': '../static/images/images.jpg' , 'percent': '40'},
            {'title': 'Sweet Melody', 'image_url': '../static/images/dinner.jpg', 'percent': '100'},
            {'title': 'Angel of Sweet death and Codiene Scene', 'image_url': '../static/images/angel.jpg', 'percent': '60'},
            {'title': 'Take me to Church', 'image_url': '../static/images/church.jpg', 'percent': '70'},
            {'title': 'Dinner', 'image_url': '../static/images/church.jpg', 'percent': '50'}
        ],
        'albums' : [
        {'title': 'Unreal Unearth', 'image_url': '../static/images/Church.jpg'},
        {'title': 'Future Nostalgia', 'image_url': '../static/images/dinner.jpg'},
        {'title': 'After Hours', 'image_url': '../static/images/angel.jpg'},
        {'title': 'Wasteland Baby!', 'image_url': '../static/images/image.jpg'},
        {'title': 'After Hours', 'image_url': '../static/images/after_hours.jpg'}
        ]
}

def artist_dashboard():
    #will have to send query to database to get the artist data
    return artist_data


def user_dashboard():
    #will have to send query to get the user data 
    return artist_data

def stats():
    #will have to send query to get artist stats
    return artist_data

def upload(request):
    upload_type = request.form.get("uploadType")
    if upload_type == "single":
            # Receive single song file from HTML form
            song_file = request.files.get("songFile")
            if song_file and song_file.filename.endswith(".mp3"):
                # Forward the file to the backend
                files = {'songFile': (song_file.filename, song_file.stream, song_file.content_type)}
                data = {'uploadType': 'single'}
                # testing, works!
                response = requests.post(get_backend_url(), files=files, data=data)

                if response.status_code == 200:
                    return True
                else:
                    return False
                
                # response = requests.post(f"{get_backend_url()}/get_music/{song_file.filename}", files=files, data=data)
                # return f"Backend Response: {response.status_code} - {response.text}"
            else:
                return "Invalid MP3 file.", 400

    elif upload_type == "album":
            # Receive album files and metadata from HTML form
            album_title = request.form.get("albumTitle")
            album_type = request.form.get("albumType")
            album_songs = request.files.getlist("albumSongs")
            
            if album_title and album_type and album_songs:
                files = []
                for song_file in album_songs:
                    if song_file.filename.endswith(".mp3"):
                        files.append(
                            ('albumSongs', (song_file.filename, song_file.stream, song_file.content_type))
                        )
                
                data = {'uploadType': 'album', 'albumTitle': album_title, 'albumType': album_type}
                
                response = requests.post(get_backend_url(), files=files, data=data)

                if response.status_code == 200:
                    return True
                else:
                    return False
                # response = requests.post(f"{get_backend_url()}/get_music/{song_file.filename}", files=files, data=data)
                # return f"Backend Response: {response.status_code} - {response.text}"
            else:
                return "Missing album details or files.", 400
            

def album():
     #should return album data
     return artist_data

def search(string):
     #query database to get one song back
     url = f'{get_backend_url()}/user/search'
     response = requests.post(url, json={"search": string})
     if response.status_code == 200:
        return response.json()
     else:
        return None
