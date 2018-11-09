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
  # path("campaign/<slug:camp_name>",
    # views.campaign, name="campaign"),

  # Create campaign view.
  path("campaign/create",
    views.create_campaign, name="create_campaign"),

  # Join campaign view.
  path("campaign/<slug:camp_name>/join",
    views.join_campaign, name="join_campaign"),

  # Continue campaign view.
  path("campaign/<slug:camp_name>/continue",
    views.continue_campaign, name="continue_campaign"),

  # User's campaign view
  path("campaign/<slug:camp_name>/<slug:usr_name>",
    views.user_view, name="user_view"),

  # Character view
  path("campaign/<slug:camp_name>/<slug:usr_name>/<slug:character_name>",
    views.character_data, name="character_data"),



  # Operation director
  path("campaign/<slug:camp_name>/<slug:usr_name>/operation/<slug:operation>",
    views.user_operation, name="user_operation"),

]
