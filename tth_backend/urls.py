from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views # To prevent mixups

from . import views

app_name = "tth"
urlpatterns = [
  path("", views.index, name="index"),
  path("main", views.lobby_view, name="main"),
  path("get_campaigns", views.get_campaigns, name="get_campaigns"),

  # Login, logout and other account views come from Django (see 'registration' -folder)
  path("accounts/", include("django.contrib.auth.urls")),

  # Continue campaign
  path("continue_campaign", views.continue_campaign, name="continue_campaign"),

  # Create campaign
  path("create_campaign/", views.create_campaign, name="create_campaign"),

  # Campaign page
  re_path(r"^campaign/(?P<campaign_name>\w+)", views.campaign_data, name="campaign"),

  # Character page
  re_path(r"^character/(?P<character_name>\w+)", views.character_data, name="character"),


]
