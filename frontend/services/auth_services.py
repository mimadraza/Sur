import requests
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #adding parent to PYTHONPATH
from Config import Config
backendurl = Config.BACKEND_URL

def validation_register(request, validation, gl):
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email": request.form["email"],
        "password" : request.form["password"],
        "country" : request.form["country"],
        "dob" : request.form["dob"]
        }
    result = gl.validate(validation, data) #returns true if all validations passed
    #differentiate between artist and user from database required or not
    #url = "http://backendserver.com/your-api-route?flag=true"
    if result.success:
        response = requests.post(backendurl, json=data)

        if response.status_code == 200:
            return True
        else:
            return False
        
def validation_login(request, validation, gl):
    data = {
        "email": request.form["email"],
        "password" : request.form["password"]
        }
    result = gl.validate(validation, data) #returns true if all validations passed
    #differentiate between artist and user from database required or not
    #url = "http://backendserver.com/your-api-route?flag=true"
    if result.success:
        response = requests.post(backendurl, json=data)

        if response.status_code == 200:
            return True
        else:
            return False
        
def profile(request, validation, gl):
    data = {
        "bio" : request.form["bio"],
        }
        
    result = gl.validate(validation, data) #returns true if all validations passed
    if result:  
            image_file = request.files.get("image")
            if image_file :
                # Forward the file to the backend
                files = {'image': (image_file.filename, image_file.stream, image_file.content_type)}
                # testing, works!
                print(files,data)
                response = requests.post(backendurl, files=files, data=data)

                if response.status_code == 200:
                    return True
                else:
                    return False
                # response = requests.post(f"{backendurl}/get_music/{image_file.filename}", files=files, data=data)
                # return f"Backend Response: {response.status_code} - {response.text}"
    else:
        return False
    

     
        