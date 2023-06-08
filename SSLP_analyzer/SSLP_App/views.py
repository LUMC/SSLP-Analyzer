from django.shortcuts import render

def home_view(request):
    return render(request, 'homepage.html')

def data_editor_view(request):
    return render(request, 'editpage.html')

def feed_view(request):
    return render(request, 'login.html')

