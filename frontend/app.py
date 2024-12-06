from flask import Flask, jsonify, request, render_template, redirect
from config import Config
# import requests
from flask_cors import CORS
# import gladiator as gl
#Use session to dictate whether artist is trying to log in or user
# from flask import session
# import os
# artist_data = {
#         'background_url': 'static/images/artistbackground.jpg',
#         'profile_url': 'static/images/Hozier.webp',
#         'Artist_rank': 12,
#         'Artist_Followers': 100,
#         'Artist_likes': 100,
#         'songs': [
#             {'title': 'Too Sweet', 'image_url': 'static/images/images.jpg' , 'percent': '40'},
#             {'title': 'Sweet Melody', 'image_url': 'static/images/dinner.jpg', 'percent': '100'},
#             {'title': 'Angel of Sweet death and Codiene Scene', 'image_url': 'static/images/angel.jpg', 'percent': '60'},
#             {'title': 'Take me to Church', 'image_url': 'static/images/church.jpg', 'percent': '70'},
#             {'title': 'Dinner', 'image_url': 'static/images/church.jpg', 'percent': '50'}
#         ],
#         'albums' : [
#         {'title': 'Unreal Unearth', 'image_url': 'static/images/Church.jpg'},
#         {'title': 'Future Nostalgia', 'image_url': 'static/images/dinner.jpg'},
#         {'title': 'After Hours', 'image_url': 'static/images/angel.jpg'},
#         {'title': 'Wasteland Baby!', 'image_url': 'static/images/image.jpg'},
#         {'title': 'After Hours', 'image_url': 'static/images/after_hours.jpg'}
#         ]
# }
app = Flask(__name__, static_folder='static')
CORS(app)
backendurl = Config.BACKEND_URL
# login_validations = (('email',gl.required, gl.format_email), ('password', gl.required))

# register_validations = (('first_name', gl.required, gl.type_(str), gl.regex_('^[^0-9]*$')),
#                         ('last_name', gl.required, gl.type_(str),gl.regex_('^[^0-9]*$')),
#                         ('email',gl.required, gl.format_email), ('password', gl.required),
#                         ('country', gl.required, gl.regex_('^[^0-9]*$')), 
#                         ('dob', gl.required))
# profile_validations = (('bio', gl.required, gl.type_(str), gl.regex_(".{20,}")))

#Need to set a secret key so that no invalid users can access session information
# app.secret_key = os.urandom(24)

from routes.auth_routes import userauth_blueprint
from routes.auth_routes import artistauth_blueprint

#JUST FOR TEST
from routes.dash_routes import userdash_blueprint 
from routes.dash_routes import artistdash_blueprint 

app.register_blueprint(userauth_blueprint, url_prefix = '/userauth')
app.register_blueprint(artistauth_blueprint, url_prefix = '/artistauth')
app.register_blueprint(artistdash_blueprint, url_prefix = '/artistdash')
app.register_blueprint(userdash_blueprint, url_prefix = '/userdash')

@app.route('/')
def index():  
    
    
    return redirect('/artistdash/dashboard')
@app.route('/login', methods=["GET","POST"])
def login():  
    #Make sure artist and user have different hits on backend SOLVED: USING SESSION
    #Get session flag:
    flag = session.get('flag', False) 
    
    if request.method == "POST":
        data = {"email" : request.form['email'],
                "password" : request.form['password']}
        return redirect('/artistdashboard')
        result = gl.validate(login_validations, data) #returns true if all validations passed
        if result:  #uncoment below once backend becomes functional
            # response = request.get_json(backendurl)
            # if (response.statuscode == 200):    
            #     return redirect("userdashboard.html")
            if flag: 
                redirect('/artistdashboard')
            else:
                redirect('/userdashboard')
        
    return render_template('LoginPage.html')

# @app.route('/userregister', methods=["GET","POST"])
# def userregister():
#     if request.method == "POST":
#         data = {
#         "first_name" : request.form["first_name"],
#         "last_name" : request.form["last_name"],
#         "email": request.form["email"],
#         "password" : request.form["password"],
#         "country" : request.form["country"],
#         "dob" : request.form["dob"]
#         }
        
#         result = gl.validate(register_validations, data) #returns true if all validations passed

#         if result.success:  #uncoment below once backend becomes functional
#             # response = request.get_json(backendurl)
#             # if (response.statuscode == 200):    
#             #     return redirect("/login")
#             return redirect('/login')
#         else:
#             return render_template('userregisterpage.html', visibility = "visible")

    
#     return render_template('userregisterpage.html', visibility = "hidden")

# @app.route('/artistregister', methods=["GET","POST"])
# def artistregister():
    
#     if request.method == "POST":
#         data = {
#         "first_name" : request.form["first_name"],
#         "last_name" : request.form["last_name"],
#         "email": request.form["email"],
#         "password" : request.form["password"],
#         "country" : request.form["country"],
#         "dob" : request.form["dob"]
#         }
        
#         result = gl.validate(register_validations, data) #returns true if all validations passed
#         if result:  #uncoment below once backend becomes functional
#             # response = request.get_json(backendurl)
#             # if (response.statuscode == 200):    
#             #     return redirect("/login")
#             return redirect('/set_flag')
    
#     return render_template('artistregister.html')

# @app.route('/profilesetup', methods=["GET","POST"])
# def profilesetup():
    
#     if request.method == "POST":
#         data = {
#         "bio" : request.form["bio"],
#         }
        
#         result = gl.validate(profile_validations, data) #returns true if all validations passed
#         if result:  #uncoment below once backend becomes functional
#             # response = request.get_json(backendurl)
#             # if (response.statuscode == 200):    
#             #     return redirect("/login")
#             print(data['bio'])
    
#     return render_template('profileSetup.html')


# @app.route('/userdashboard', methods=['GET', 'POST'])
# def userdashboard():

#     return render_template('userdashboard.html', artist_data = artist_data)

# @app.route('/artistdashboard', methods=['GET', 'POST'])
# def artistdashboard():
#     #define this as a global array in a seperate route where data is moved for both user and artist.
    
#     return render_template('artistdashboard.html', artist_data = artist_data)


# @app.route('/set_flag')
# def set_flag():
#     # Flag true means artist is trying to login, else user
#     session['flag'] = True
#     return redirect('/login')

@app.route('/get_music_from_backend/<song_name>')
def get_music_from_backend(song_name):
    # Request the song from the backend app
    response = requests.get(f"{backendurl}/get_music/{song_name}")


    if response.status_code == 200:
        return response.content  # This sends the raw binary data of the MP3 file
    else:
        return "Error fetching song", 404

@app.route('/send_music_to_backend/<song_name>')
def send_music_to_backend(song_name):
    
    return 'Hello'


@app.route('/stats')
def stats():
    # Render the stats page (you can add actual stats data here)
    return render_template('Analytics.html',artist_data = artist_data)

# @app.route('/discover')
# def discover():
#     # Render the discover page
#     return render_template('discover.html')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == "POST":
#         upload_type = request.form.get("uploadType")
        
#         if upload_type == "single":
#             # Receive single song file from HTML form
#             song_file = request.files.get("songFile")
#             if song_file and song_file.filename.endswith(".mp3"):
#                 # Forward the file to the backend
#                 files = {'songFile': (song_file.filename, song_file.stream, song_file.content_type)}
#                 data = {'uploadType': 'single'}
#                 # testing, works!
#                 print(files,data)
                
#                 response = requests.post(f"{backendurl}/get_music/{song_file.filename}", files=files, data=data)
#                 return f"Backend Response: {response.status_code} - {response.text}"
#             else:
#                 return "Invalid MP3 file.", 400

#         elif upload_type == "album":
#             # Receive album files and metadata from HTML form
#             album_title = request.form.get("albumTitle")
#             album_type = request.form.get("albumType")
#             album_songs = request.files.getlist("albumSongs")
            
#             if album_title and album_type and album_songs:
#                 files = []
#                 for song_file in album_songs:
#                     if song_file.filename.endswith(".mp3"):
#                         files.append(
#                             ('albumSongs', (song_file.filename, song_file.stream, song_file.content_type))
#                         )
                
                data = {'uploadType': 'album', 'albumTitle': album_title, 'albumType': album_type}
                response = requests.post(f"{backendurl}/get_music/{song_file.filename}", files=files, data=data)
                return f"Backend Response: {response.status_code} - {response.text}"
            else:
                return "Missing album details or files.", 400
    else:
        return render_template('upload.html')
    
@app.route('/album_page')
def album_page():
    return render_template('albums.html', artist_data = artist_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)