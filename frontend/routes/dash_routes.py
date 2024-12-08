from flask import Blueprint, request, redirect, render_template
from frontend.services import dash_services

userdash_blueprint = Blueprint('userdash', __name__)
artistdash_blueprint = Blueprint('artistdash', __name__)

@userdash_blueprint.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    user_data = dash_services.user_dashboard()
    return render_template('userdashboard.html', artist_data = user_data)

@artistdash_blueprint.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    user_data = dash_services.artist_dashboard()
    print(user_data)
    
    return render_template('artistdashboard.html', artist_data = user_data)

@artistdash_blueprint.route('/stats', methods = ['GET', 'POST'])
def stats():
    user_data = dash_services.stats()

    return render_template('Analytics.html', artist_data = user_data)

@artistdash_blueprint.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        dash_services.upload(request)
    else:
        return render_template('upload.html')

@artistdash_blueprint.route('/album', methods = ['GET', 'POST'])
def album():
    artist_album = dash_services.album()
    return render_template('albums.html', artist_data = artist_album)

@userdash_blueprint.route('/album', methods = ['GET', 'POST'])
def album():
    artist_album = dash_services.album()
    return render_template('albums.html', artist_data = artist_album)

@userdash_blueprint.route('/search', methods = ['POST'])
def search():
    result = dash_services.search(request.form['search'])
    return render_template('searchpage.html', artist_data = result)