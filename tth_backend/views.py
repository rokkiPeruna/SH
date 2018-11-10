from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
# To prevent unauthorized access to views
from django.contrib.auth.decorators import login_required

# Models
from .models import Campaign, User
# Managers
from .models import CampaignManager, CharacterManager

######################################################################
# First place to land, the index which directs directly to login page.
# Login view is from Django, login.html is in root/registration/login.html
######################################################################
from dummyserver.settings import *
def index(request):
  return HttpResponseRedirect("accounts/login")


# # # # # # # # # # # # # #
# LOBBY PAGE FUNCTIONALITY
# # # # # # # # # # # # # #

CAMPAIGN_OPERATIONS = {
  "CONTINUE": "continue",
  "JOIN": "join",
  "CREATE": "create"
}

######################################################################
# After successful login, the lobby awaits
######################################################################
@login_required
def lobby_view(request):
  response = {
    "logged_user": request.user.username,
    "allcampaigns": Campaign.objects.all(),
    "campaigns": request.user.campaigns.all(),
  }
  return render(request, "main_lobby.html", response)


######################################################################
# Get current user's data (characters, etc.)
######################################################################
@login_required
def get_user_data(request):
  pass

######################################################################
# Update user data
######################################################################
@login_required
def update_user_data(request):
  pass



# # # # # # # # # # # # # # # #
# CAMPAIGN PAGE FUNCTIONALITY
# # # # # # # # # # # # # # # #

######################################################################
# Campaign view TODO: Necessary?
######################################################################
@login_required
def campaign(request, camp_name):
    return HttpResponse("Wai u hier?")

######################################################################
# Create a new campaign
######################################################################
@login_required
def create_campaign(request):
  # Check that all necessary data is present
  camp_name = request.POST["new-camp-name"]
  gm_pw = request.POST["new-camp-gmpw"]
  pl_pw = request.POST["new-camp-pw"]
  sdesc = request.POST["new-camp-sdesc"]
  if None in (camp_name, gm_pw, pl_pw, sdesc):
    return HttpResponseBadRequest("Invalid args, failed to create campaign with name '{}'".format(camp_name))
  else:
    result = CampaignManager.add_campaign(request.user, camp_name, gm_pw, pl_pw, sdesc)
    if result[0] != False:
      return redirect("tth:user_view", camp_name=camp_name, usr_name=request.user.username)
    else:
      return HttpResponse("Failed to create campaign '{}'. Error: {}".format(camp_name, result[1]))


######################################################################
# Continue on-going campaign
######################################################################
@login_required
def continue_campaign(request, camp_name):
  campaign = CampaignManager.get_campaign_by_name(camp_name)
  if campaign != False:
    return redirect("tth:user_view", camp_name=camp_name, usr_name=request.user.username)
  else:
    return HttpResponse("Failed to continue '{}' campaign".format(camp_name))


######################################################################
# Join on-going campaign
######################################################################
@login_required
def join_campaign(request):
  # Check that all necessary data is available
  camp_name = request.POST.get("join-camp-name", False)
  camppw = request.POST.get("join-camp-pw", False)
  if False in (camp_name, camppw):
    return HttpResponseBadRequest("Invalid arguments")
  else:
    # CampaignManager knows if password is valid
    success, campaign = CampaignManager.join_campaign(request.user, camp_name, camppw)
    if success:
      return redirect("tth:user_view", camp_name=campaign.name, usr_name=request.user.usr_name)
    else:
      return HttpResponseBadRequest("Failed to join '{}' campaign".format(camp_name))


######################################################################
# User's view to campaign and characters etc.
######################################################################
@login_required
def user_view(request, camp_name, usr_name):
  campaign = CampaignManager.get_campaign_by_name(camp_name)
  story = campaign.story # TODO Check campaign sanity
  notes = "dummy notes" # TODO Get user notes
  response = {
    "logged_user": request.user.username,
    "camp_name": campaign.name,
    "campaign_story": story,
    "campaign_notes": notes,
    "characters": CharacterManager.get_user_characters(request.user),
    # "characters": CharacterManager.get_campaign_characters(campaign),
  }
  return render(request, "campaign_lobby.html", response)


######################################################################
# User performed operation
######################################################################
@login_required
def user_operation(request, camp_name, usr_name, operation):
  if operation == "create_character" and request.method == "POST":
    char_name = request.POST.get("char-name", "default name")
    CharacterManager.create_character(request.user, char_name)
    return redirect("tth:character_data", camp_name=camp_name, usr_name=usr_name, character_name=char_name)
  else:
    return HttpResponseBadRequest("No such operation")

######################################################################
# Campaign character(s). Regular player see her/his character and
# public NPCs, gamemaster sees everything
######################################################################
@login_required
def character_data(request, camp_name, usr_name, character_name):
  return render(request, "modify_character.html", {})
  return HttpResponse("Char created: {} {} {}".format(camp_name, usr_name, character_name))
