from flask import Blueprint, request, redirect, render_template
import gladiator as gl
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #adding parent to PYTHONPATH
from services import auth_services

userauth_blueprint = Blueprint('userauth', __name__)
artistauth_blueprint = Blueprint('artistauth', __name__)

login_validations = (('email',gl.required, gl.format_email), ('password', gl.required))
register_validations = (('first_name', gl.required, gl.type_(str), gl.regex_('^[^0-9]*$')),
                        ('last_name', gl.required, gl.type_(str),gl.regex_('^[^0-9]*$')),
                        ('email',gl.required, gl.format_email), ('password', gl.required),
                        ('country', gl.required, gl.regex_('^[^0-9]*$')), 
                        ('dob', gl.required))
profile_validations = (('bio', gl.required, gl.type_(str), gl.regex_(".{20,}")))


@userauth_blueprint.route('/register', methods = ['GET', 'POST'])
def register ():
    if request.method == "POST":
       if auth_services.validation_register(request, register_validations, gl):
            return redirect('/userauth/login')
       else:
            return render_template('userregisterpage.html')

    
    return render_template('userregisterpage.html')


@userauth_blueprint.route('/login', methods = ['GET', 'POST'])
def login ():
    if request.method == "POST":
       if auth_services.validation_login(request, login_validations, gl):
            return redirect('/userdash/dashboard')
       else:
            return render_template('Loginpage.html')

    
    return render_template('Loginpage.html')




@artistauth_blueprint.route('/register', methods = ['GET', 'POST'])
def register ():
    if request.method == "POST":
       if auth_services.validation_register(request, register_validations, gl):
            return redirect('/artistauth/profile')
       else:
            return render_template('artistregister.html')

    
    return render_template('artistregister.html')


@artistauth_blueprint.route('/profile', methods = ['GET', 'POST'])
def profile ():
    if request.method == "POST":
       if auth_services.profile(request, profile_validations, gl):
            return redirect('/artistdash/dashboard')
       else:
            return render_template('Loginpage.html')

    
    return render_template('profileSetup.html')


@artistauth_blueprint.route('/login', methods = ['GET', 'POST'])
def login ():
    if request.method == "POST":
       if auth_services.validation_login(request, login_validations, gl):
            return redirect('/artistdash/dashboard')
       else:
            return render_template('Loginpage.html')

    
    return render_template('Loginpage.html')











