def validation(request, validation, gl):
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email": request.form["email"],
        "password" : request.form["password"],
        "country" : request.form["country"],
        "dob" : request.form["dob"]
        }
    result = gl.validate(validation, data) #returns true if all validations passed

    if result.success:  #uncoment below once backend becomes functional
        # response = request.get_json(backendurl)
        # if (response.statuscode == 200):    
        #     return redirect("/login")
        return True
    
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
                data = {'uploadType': 'single'}
                # testing, works!
                print(files,data)
                
                # response = requests.post(f"{backendurl}/get_music/{image_file.filename}", files=files, data=data)
                # return f"Backend Response: {response.status_code} - {response.text}"
            else:
                return "Invalid image.", 400
            
            
            
            #uncoment below once backend becomes functional
            # response = request.get_json(backendurl)
            # if (response.statuscode == 200):    
            #     return redirect("/login")
            return True
    

     
        