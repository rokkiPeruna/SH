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
def campaign(request, campaign_name):
    return HttpResponse("Wai u hier?")

######################################################################
# Create a new campaign
######################################################################
@login_required
def create_campaign(request):
  # Check that all necessary data is present
  cname = request.POST["new-camp-name"]
  gm_pw = request.POST["new-camp-gmpw"]
  pl_pw = request.POST["new-camp-pw"]
  sdesc = request.POST["new-camp-sdesc"]
  if None in (cname, gm_pw, pl_pw, sdesc):
    return HttpResponseBadRequest("Invalid args, failed to create campaign with name '{}'".format(cname))
  else:
    result = CampaignManager.add_campaign(request.user, cname, gm_pw, pl_pw, sdesc)
    if result[0] != False:
      return redirect("tth:userview", campaign_name=cname, username=request.user.username)
    else:
      return HttpResponse("Failed to create campaign '{}'. Error: {}".format(cname, result[1]))


######################################################################
# Continue on-going campaign
######################################################################
@login_required
def continue_campaign(request, campaign_name):
  qlist = request.user.campaigns.filter(name__exact=campaign_name)
  if qlist != None and qlist.count():
    campaign = CampaignManager.get_campaign_by_name(campaign_name)
    return redirect("tth:userview", campaign_name=campaign_name, username=request.user.username)
  else:
    return False, "Failed to join campaign"


######################################################################
# Join on-going campaign
######################################################################
@login_required
def join_campaign(request):
  # Check that all necessary data is available
  cname = request.POST.get("join-camp-name", False)
  camppw = request.POST.get("join-camp-pw", False)
  if False in (cname, camppw):
    return HttpResponseBadRequest("Invalid arguments")
  else:
    # CampaignManager knows if password is valid
    success, campaign = CampaignManager.join_campaign(request.user, cname, camppw)
    if success:
      return redirect("tth:userview", campaign_name=campaign.name, username=request.user.username)
    else:
      return HttpResponseBadRequest("Failed to join '{}' campaign".format(cname))


######################################################################
# User's view to campaign and characters etc.
######################################################################
@login_required
def userview(request, campaign_name, username):
  campaign = CampaignManager.get_campaign_by_name(campaign_name)
  story = campaign.story # TODO Check campaign sanity
  notes = "dummy notes" # TODO Get user notes
  response = {
    "logged_user": request.user.username,
    "campaign_name": campaign.name,
    "campaign_story": story,
    "campaign_notes": notes,
    "characters": ["jds", "sfeds", "adsa"],
    # "characters": CharacterManager.get_campaign_characters(campaign),
  }
  return render(request, "campaign_lobby.html", response)


######################################################################
# Campaign character(s). Regular player see her/his character and
# public NPCs, gamemaster sees everything
######################################################################
@login_required
def character_data(request, character_name):
  pass
