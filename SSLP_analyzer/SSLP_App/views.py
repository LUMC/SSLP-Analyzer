from django.shortcuts import render

def home_view(request):
    context = {
        "user": request.user,
    }
    return render(request, 'homepage.html', context)

def data_editor_view(request):
    return render(request, 'editpage.html')

def feed_view(request):
    return render(request, 'login.html')

