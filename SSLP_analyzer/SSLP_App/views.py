from django.shortcuts import render

def home_view(request):
    return render(request, 'homepage.html')

def data_editor_view(request):
    
    dummy = [{"haplo":"Test", "chr":"4","SSLP":"162","percent":"0.60","perm":"1"} for _ in range(25)]
    return render(request, 'editpage.html',{"table":dummy})

def feed_view(request):
    return render(request, 'login.html')

