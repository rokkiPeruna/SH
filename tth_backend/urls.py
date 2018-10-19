from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views # To prevent mixups

from . import views

app_name = "tth"
urlpatterns = [
  path("", views.index, name="index"),
  path("main", views.main_view, name="main"),
  path("campaigns", views.get_campaigns, name="get_campaigns"),
  path("accounts/", include("django.contrib.auth.urls")),
  # Change the URL for login so we don't need separate 'registration' -folder
  path("login/", auth_views.LoginView.as_view()),

]
