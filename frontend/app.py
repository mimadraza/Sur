from flask import Flask, render_template, redirect
from config import Config

from flask_cors import CORS

#Use session to dictate whether artist is trying to log in or user
# from flask import session
# import os

app = Flask(__name__, static_folder='static')
CORS(app)
backendurl = Config.BACKEND_URL

#note FROM SAAD:
#THESE ROUTES AND BLUEPRINTS WILL NOT EXIST IN FINAL APP.PY ARE JUST THERE FOR TROUBLESHOOTING HTML PAGES 
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
    
    
    return redirect('/userdash/dashboard')

# @app.route('/get_music_from_backend/<song_name>')
# def get_music_from_backend(song_name):
#     # Request the song from the backend app
#     response = requests.get(f"{backendurl}/get_music/{song_name}")


#     if response.status_code == 200:
#         return response.content  # This sends the raw binary data of the MP3 file
#     else:
#         return "Error fetching song", 404

# @app.route('/send_music_to_backend/<song_name>')
# def send_music_to_backend(song_name):
    
#     return 'Hello'


# @app.route('/stats')
# def stats():
#     # Render the stats page (you can add actual stats data here)
#     return render_template('Analytics.html',artist_data = artist_data)

    
@app.route('/album_page')
def album_page():
    return render_template('albums.html', artist_data = artist_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)