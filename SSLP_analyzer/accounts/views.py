from django.shortcuts import render

def login_and_register_view(request):
    return render(request, 'temp.html')

def logout_view(request):
    return render(request, 'temp.html')
