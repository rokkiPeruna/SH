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

  # Campaign view.
  path("campaign/<slug:campaign_name>",
    views.campaign, name="campaign"),

  # Create campaign view.
  path("campaign/create/",
    views.create_campaign, name="create_campaign"),

  # Join campaign view.
  path("campaign/<slug:campaign_name>/join",
    views.join_campaign, name="join_campaign"),

  # Continue campaign view.
  path("campaign/<slug:campaign_name>/continue",
    views.continue_campaign, name="continue_campaign"),

  # Participants's campaign view
  path("campaign/<slug:campaign_name>/<slug:participant>",
    views.participant, name="participant"),

  # Character view
  path("campaign/<slug:campaign_name>/<slug:participant>/<slug:character>",
    views.character_data, name="character"),


]
