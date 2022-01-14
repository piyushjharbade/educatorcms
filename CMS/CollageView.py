from django.shortcuts import render

def CollageInterface(request):
    return render(request,"collage.html")

def About(request):
    return render(request,"About.html")

def Course(request):
    return render(request,"collagecourse.html")

def Blog(request):
    return render(request,"Blog.html")

def Contact(request):
    return render(request,"contact.html")

def Login(request):
    return render(request,"Login.html",{'msg':''})

def SLogin(request):
    return render(request,"Slogin.html",{'msg':''})