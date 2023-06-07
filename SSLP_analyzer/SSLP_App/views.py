from django.shortcuts import render

def home_view(request):
    return render(request, 'temp.html')

def data_editor_view(request):
    return render(request, 'temp.html')

def feed_view(request):
    return render(request, 'temp.html')


