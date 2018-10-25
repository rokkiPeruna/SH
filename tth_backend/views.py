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
    "mycampaigns": request.user.mycampaigns.all(),
    # Campaign operations
    "coper_continue": CAMPAIGN_OPERATIONS["CONTINUE"],
    "coper_join": CAMPAIGN_OPERATIONS["JOIN"],
    "coper_create": CAMPAIGN_OPERATIONS["CREATE"]
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
# Campaign view TODO: Separate game master and player!
# 'campaign_name' is the campaign which the 'operation' targets.
# Valid operations:
# "join"
# "create"
# "continue"
######################################################################
@login_required
def campaign(request, campaign_name, operation):
  # Success indicator and payload which is response
  result = (False, "Keijo")
  if request.method == "POST":
    if operation == CAMPAIGN_OPERATIONS["CREATE"]:
      result = _create_campaign(request)
    elif operation == CAMPAIGN_OPERATIONS["JOIN"]:
      result = _join_campaign(request)
  elif request.method == "GET":
    if operation == CAMPAIGN_OPERATIONS["CONTINUE"]:
      result = _continue_campaign(request, campaign_name)
  else:
    result = (False, "Invalid HTTP operation for campaign")

  if result[0] == True:
    # TODO: LOG SUCCESS
    # logger.info("Performed operation '{}' with campaign '{}'")
    return render(request, "campaign_lobby.html", result[1])
  else:
    # TODO: LOG FAILURE
    # logger.info("Operation '{}' FAILED with campaign '{}'")
    return HttpResponse(operation +"!"+campaign_name)


######################################################################
# Create a new campaign
######################################################################
@login_required
def _create_campaign(request):
  # Check that all necessary data is present
  cname = request.POST.get("new-camp-name")
  gm_pw = request.POST.get("new-camp-gmpw")
  pl_pw = request.POST.get("new-camp-pw")
  sdesc = request.POST.get("new-camp-sdesc")
  if None in (cname, gm_pw, pl_pw, sdesc):
    return False, "Invalid args, failed to create campaign with name '{}'".format(cname)
  else:
    campaign = CampaignManager.add_campaign(request.user, cname, gm_pw, pl_pw, sdesc)
    if campaign != False:
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
      # Parse 'new' from URL
      return (True, response)
    else:
      return (False, "Failed to create campaign '{}'".format(cname))


######################################################################
# Continue on-going campaign
######################################################################
@login_required
def _continue_campaign(request, campaign_name):
  # Check that user is participant of the given campaign before redirecting
  qlist = request.user.mycampaigns.filter(name__exact=campaign_name)
  if qlist != None and qlist.count():
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
    return (True, response)
  else:
    return (False, "Failed to join campaign")


######################################################################
# Join on-going campaign
######################################################################
@login_required
def _join_campaign(request):
  # Check that all necessary data is available
  cname = request.POST.get("join-camp-name", False)
  camppw = request.POST.get("join-camp-pw", False)
  if False in (cname, camppw):
    return False, "Invalid arguments"
  else:
    # CampaignManager knows if password is valid
    success, msg = CampaignManager.join_campaign(request.user, cname, camppw)
    if success:
      campaign = msg#contains the campaign model
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
      return (True, response)
    else:
      return (False, "Failed to join '{}' campaign".format(cname))


######################################################################
#
######################################################################
def user_camp_view(request, campaign_name, user_name):
  pass


######################################################################
# Campaign character(s). Regular player see her/his character and
# public NPCs, gamemaster sees everything
######################################################################
@login_required
def character_data(request, character_name):
  pass
