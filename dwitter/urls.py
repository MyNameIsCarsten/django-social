from django.urls import path

# import a view functions called dashboard, profile_list and profile from your app’s views.py
from .views import dashboard, profile_list, profile

app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    
    # route requests that come to /profile_list to the view function called profile_list()
    path("profile_list/", profile_list, name="profile_list"),

    # angled-bracket syntax allows you to capture path components
    path("profile/<int:pk>", profile, name="profile"),
]