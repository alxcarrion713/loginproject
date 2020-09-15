from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return HttpResponse("Yo Arod")

def index(request):
    return render(request, "index.html")

def register(request):
    print(request.POST)
    validationErrors = User.objects.registrationValidator(request.POST)
    print(validationErrors)
    if len(validationErrors)>0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hashedPw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
        newuser= User.objects.create(first_name= request.POST['fname'],last_name= request.POST['lname'], email= request.POST['email'], password= hashedPw)
        print(newuser)
        request.session['loggedinid'] = newuser.id
    return redirect("/success")

def success(request):
    if 'loggedinid' not in request.session:
        return redirect("/")
    loggedinuser= User.objects.get(id= request.session['loggedinid'])
    context={
        'loggedinuser' : loggedinuser
    }
    return render(request, "success.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def login(request):
    print(request.POST)
    validation_errors = User.objects.loginValidator(request.POST)
    print(validation_errors)
    if len(validation_errors) > 0:
        for key, value in validation_errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        user = User.objects.filter(email = request.POST['email'])[0]
        request.session['loggedinid']= user.id
        return redirect('/success')