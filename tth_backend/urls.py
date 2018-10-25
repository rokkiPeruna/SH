from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views # To prevent mixups

from . import views

app_name = "tth"
urlpatterns = [
  # Redirects to accounts and login
  path("", views.index, name="index"),

  # Main lobby view. Join, continue and create campaigns
  path("main", views.lobby_view, name="main"),

  # Login, logout and other account views come from Django (see 'registration' -folder)
  path("accounts/", include("django.contrib.auth.urls")),

  # Campaign view
  re_path(r"^campaign/(?P<campaign_name>\w+)/(?P<operation>\w+)", views.campaign, name="campaign"),

  # User's campaign view
  re_path(r"^campaign/(?P<campaign_name>)/(?P<user_name>\w+)/", views.user_camp_view, name="user_camp_view"),

  # Character view
  re_path(r"^character/(?P<character_name>\w+)", views.character_data, name="character"),


]
