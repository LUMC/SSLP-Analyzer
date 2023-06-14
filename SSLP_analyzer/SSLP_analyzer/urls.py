"""
URL configuration for SSLP_analyzer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from SSLP_App.views import(
    home_view,
    data_editor_view,
    feed_view,
)

from accounts.views import (
    login_and_register_view,
    logout_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='homepage'),
    path('data-editor/', data_editor_view, name="data_editor"),
    path('feed/', feed_view, name="feed"),
    path("signin/", login_and_register_view, name="signin"),
    path("logout/", logout_view, name="logout"),
]
