<<<<<<< HEAD
from flask import Flask, request, render_template, redirect
from config import Config
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)
=======
import requests
from flask import Flask, render_template
from config import Config

app = Flask(__name__)
>>>>>>> 98a7967620d1c8822cf44d13ce2d4c37fa90eeee
backendurl = Config.BACKEND_URL


@app.route('/')
def index():  
    return redirect('/login') #Good practice

@app.route('/login', methods=["GET","POST"])
def login():  
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print(username ,email, password)
        return 'JSONOSCAS'
    
    return render_template('LoginPage.html')

@app.route('/register', methods=["GET","POST"])
def register():  
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        country = request.form["country"]
        dob = request.form["dob"]
        print(first_name, last_name)
    
    return render_template('registerpage.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
