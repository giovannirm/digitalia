# here we are import path from in-built django-urls
from django.urls import path

# here we are importing all the Views from the views.py file
from .views import *

# a list of all the urls
urlpatterns = [
    path("", home, name="home"),
]