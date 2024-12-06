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
    
def prof_validation(request, validation, gl):
    data = {
        "bio" : request.form["bio"],
        }
        
    result = gl.validate(validation, data) #returns true if all validations passed
    if result:  #uncoment below once backend becomes functional
            # response = request.get_json(backendurl)
            # if (response.statuscode == 200):    
            #     return redirect("/login")
            return True
        