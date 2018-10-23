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
  re_path(r"^continue_campaign/(?P<campaign_name>\w+)/$", views.continue_campaign, name="continue_campaign"),

  # Join campaign
  re_path(r"^join_campaign/(?P<campaign_name>\w+)", views.join_campaign, name="join_campaign"),

  # Create campaign
  path("create_campaign", views.create_campaign, name="create_campaign"),

  # Campaign page
  # re_path(r"^campaign/(?P<campaign_name>\w+)", views.campaign_data, name="campaign_data"),
  re_path(r"^campaign_data/(?P<campaign_name>)", views.campaign_data, name="campaign_data"),

  # Campaign lobby
  # re_path(r"^campaign/(?P<campaign_name>\w+)"+"/lobby", views.campaign_lobby, name="campaign_lobby"),
  re_path(r"^campaign_lobby/(?P<campaign_name>)", views.campaign_lobby, name="campaign_lobby"),

  # Character page
  re_path(r"^character/(?P<character_name>\w+)", views.character_data, name="character"),


]
