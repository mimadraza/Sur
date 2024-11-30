from flask import Flask, request, render_template, redirect
from config import Config
from flask_cors import CORS
import gladiator as gl
#Use session to dictate whether artist is trying to log in or user
from flask import session
import os

app = Flask(__name__, static_folder='static')
CORS(app)
backendurl = Config.BACKEND_URL
login_validations = (('email',gl.required, gl.format_email), ('password', gl.required) )

register_validations = (('first_name', gl.required, gl.type_(str), gl.regex_('^[^0-9]*$')),
                        ('last_name', gl.required, gl.type_(str),gl.regex_('^[^0-9]*$')),
                        ('email',gl.required, gl.format_email), ('password', gl.required),
                        ('country', gl.required, gl.regex_('^[^0-9]*$')), 
                        ('dob', gl.required))

#Need to set a secret key so that no invalid users can access session information
app.secret_key = os.urandom(24)

@app.route('/')
def index():  
    return render_template('homepage.html') 

@app.route('/login', methods=["GET","POST"])
def login():  
    #Make sure artist and user have different hits on backend SOLVED: USING SESSION
    #Get session flag:
    flag = session.get('flag', False) 
    
    if request.method == "POST":
        data = {"email" : request.form['email'],
                "password" : request.form['password']}
        
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

        if result.success:  #uncoment below once backend becomes functional
            # response = request.get_json(backendurl)
            # if (response.statuscode == 200):    
            #     return redirect("/login")
            return redirect('/login')
        else:
            return render_template('userregisterpage.html', visibility = "visible")

    
    return render_template('userregisterpage.html', visibility = "hidden")

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
        if result:  #uncoment below once backend becomes functional
            # response = request.get_json(backendurl)
            # if (response.statuscode == 200):    
            #     return redirect("/login")
            return redirect('/set_flag')
    
    return render_template('artistregister.html')

@app.route('/userdashboard', methods=['GET', 'POST'])
def userdashboard():

    return render_template('userdashboard.html')

@app.route('/artistdashboard', methods=['GET', 'POST'])
def artistdashboard():

    return render_template('artistdashboard.html')


@app.route('/set_flag')
def set_flag():
    # Flag true means artist is trying to login, else user
    session['flag'] = True
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, port=5001)