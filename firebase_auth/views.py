from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
import pyrebase
# import firebase_admin
# from firebase_admin import credentials
from django.contrib.auth import logout

# Create your views here.

# Initialising auth and firebase for further use
config={
    'apiKey': settings.API_KEY,
    'authDomain': settings.AUTH_DOMAIN,
    'databaseURL': settings.DATABASEURL,
    'projectId': settings.PROJECTID,
    'storageBucket': settings.BUCKET,
    'messagingSenderId': settings.MSG_ID,
    'appId': settings.APP_ID
}


# Get a reference to the auth service
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()


def home(request):
    if not request.session.get('uid'):
        return render(request,"Login.html")
    else:
        return render(request,"Home.html")


def signIn(request):
    if request.session.get('uid'):
        return redirect('/') 
    return render(request,"Login.html")
 

def postsignIn(request):
    if request.method == "POST":
        email=request.POST.get('email')
        pasw=request.POST.get('pass')
        try:
            # if there is no error then signin the user with given email and password
            user = authe.sign_in_with_email_and_password(email=email, password=pasw)
            if user:
                session_id=user['idToken']
                request.session['uid']=str(session_id)
                return redirect('/') 
        except Exception as e:
            message="Invalid Credentials!!Please ChecK your Data"
            return render(request,"Login.html",{"message":message})

        
 

def logout(request): 
    try:
        del request.session['uid']
    except Exception as e:
        messages.error(request, e)

    return redirect("/signin")
 

def signUp(request):
    return render(request,"Registration.html")
 

def postsignUp(request): 
    try:
        authe = firebase.auth()
        email = request.POST.get('email')
        password = request.POST.get('pass')
        confirm_password = request.POST.get('pass-repeat')
        name = request.POST.get('name')
        # try:
            # creating a user with the given email and password
        if len(password) < 8:
            messages.error(request, "Password length should more than 8 ")
            return render(request, "Registration.html")
        
        if confirm_password != password:
            messages.error(request, "Password & confirm_password Not Matching")
            return render(request, "Registration.html")
        
        user = authe.create_user_with_email_and_password(email=email, password= password)
        if user:
            session_id=user['idToken']
            request.session['uid']=str(session_id)

    except Exception as e:
        return render(request, "Registration.html", e)
    
    return render(request,"Login.html")

