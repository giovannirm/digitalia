# here we are import path from in-built django-urls
from django.urls import path

# here we are importing all the Views from the views.py file
from .views import *

# a list of all the urls
urlpatterns = [
    path("upload-csv/", upload_csv, name="upload_csv"),
    path("user-authenticate/", user_authenticate, name="user_authenticate"),
    path("user-logout/", user_logout, name="user_logout"),
]