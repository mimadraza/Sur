from flask import Flask, request, render_template, redirect
from config import Config
from flask_cors import CORS
import gladiator as gl

app = Flask(__name__, static_folder='static')
CORS(app)
backendurl = Config.BACKEND_URL
login_validations = (('email',gl.required, gl.format_email), ('password', gl.required) )
register_validations = (('first_name', gl.required, gl.type_(str)),('last_name', gl.required, gl.type_(str)),
                        ('email',gl.required, gl.format_email), ('password', gl.required), ('country', gl.required), ('dob', gl.required))


@app.route('/')
def index():  
    return render_template('userdashboard.html') #Good practice

@app.route('/login', methods=["GET","POST"])
def login():  
    #Make sure artist and user have different hits on backend
    
    if request.method == "POST":
        data = {"email" : request.form['email'],
                "password" : request.form['password']}
        
        result = gl.validate(login_validations, data) #returns true if all validations passed
        if result :  
            response = request.get_json(backendurl)
            if (response.statuscode == 200):    
                return redirect("userdashboard.html")
        
    return render_template('LoginPage.html')

@app.route('/userregister', methods=["GET","POST"])
def userregister():
    if request.method == "POST":
        data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email": request.form["email"],
        "password" : request.form["password"],
        "country" : request.form["country"],
        "dob" : request.form["dob"]
        }
        
        result = gl.validate(register_validations, data) #returns true if all validations passed
        if result :  
            response = request.get_json(backendurl)
            if (response.statuscode == 200):    
                return redirect("LoginPage.html")
    
    return render_template('userregisterpage.html')

@app.route('/artistregister', methods=["GET","POST"])
def artistregister():
    if request.method == "POST":
        data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email": request.form["email"],
        "password" : request.form["password"],
        "country" : request.form["country"],
        "dob" : request.form["dob"]
        }
        
        result = gl.validate(register_validations, data) #returns true if all validations passed
        if result :  
            response = request.get_json(backendurl)
            if (response.statuscode == 200):    
                return redirect("artistdashboard.html")
    
    return render_template('artistregister.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)