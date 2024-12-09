import requests
from flask import current_app, request

artist_data = {
    'name': 'Hozier',
    'Artist_rank':1,
    'image_url': '/static/images/Hozier.webp',
    'likes': 2100000,
    'followers': 35000000,
    'songs': [
        {
            'title': 'Take Me to Church',
            'duration': '4:01',
            'url': '/static/images/church.jpg'
        },
        {
            'title': 'Cherry Wine',
            'duration': '4:00',
            'url': '/static/images/angel.jpg'
        },
        {
            'title': 'From Eden',
            'duration': '3:41',
            'url': '/static/images/dinner.jpg'
        },
        {
            'title': 'Dinner and Diatribes',
            'duration': '4:06',
            'url': '/static/images/church.jpg'
        },
        {
            'title': 'Almost (Sweet Music)',
            'duration': '3:56',
            'url': '/static/images/church.jpg'
        }
    ],
    'albums': [
        {
            'title': 'Hozier',
            'release_date': '2014-09-19',
            'url': '/static/images/church.jpg',
            'tracks': [
                'Take Me to Church', 'From Eden', 'Cherry Wine', 'Jackie and Wilson', 'Someone New'
            ]
        },
        {
            'title': 'Wasteland, Baby!',
            'release_date': '2019-03-01',
            'url': '/static/images/church.jpg',
            'tracks': [
                'Movement', 'Almost (Sweet Music)', 'Dinner and Diatribes', 'Would That I', 'Sunlight'
            ]
        },
        {
            'title': 'Wasteland, Baby!',
            'release_date': '2019-03-01',
            'url': '/static/images/church.jpg',
            'tracks': [
                'Movement', 'Almost (Sweet Music)', 'Dinner and Diatribes', 'Would That I', 'Sunlight'
            ]
        },
        {
            'title': 'Wasteland, Baby!',
            'release_date': '2019-03-01',
            'url': '/static/images/church.jpg',
            'tracks': [
                'Movement', 'Almost (Sweet Music)', 'Dinner and Diatribes', 'Would That I', 'Sunlight'
            ]
        }
    ]
}



# Access the backend URL
def get_backend_url():
    # Access the configuration when needed
    return current_app.config['BACKEND_URL']
    """Return the URL of the backend service, as configured in the Flask app."""
    

#artist data and user_data should be globally declared


def artist_dashboard():
    url = f'{get_backend_url()}/artist/home'
    response = requests.get(url, cookies=request.cookies)
    return artist_data


def user_dashboard():
    
    url =f'{get_backend_url()}/user/home'
    response = requests.get(url, cookies=request.cookies)
    return response
   

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
            

def user_album():
     #should return album data
        url =f'{get_backend_url()}/user/home'
        response = requests.get(url, cookies=request.cookies)
        return response

def search(string):
     #query database to get one song back
     url = f'{get_backend_url()}/user/search'
     response = requests.post(url, json={"search": string})
     if response.status_code == 200:
        return response.json()
     else:
        return None
