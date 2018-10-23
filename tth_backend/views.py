from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
# To prevent unauthorized access to views
from django.contrib.auth.decorators import login_required

# Models
from .models import Campaign, User
# Managers
from .models import CampaignManager

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


######################################################################
# After successful login, the lobby awaits
######################################################################
@login_required
def lobby_view(request):
  response = {
    "logged_user": request.user.username,
    "allcampaigns": Campaign.objects.all(),
    "mycampaigns": request.user.mycampaigns.all()
  }
  return render(request, "main_lobby.html", response)


######################################################################
# Get all available campaigns
######################################################################
@login_required
def get_campaigns(request):
  if request.method == "GET":
    campaigns = Campaign.objects.all()
    context = {
      "campaigns": campaigns
    }
    return HttpResponse(context, content_type="application/json")

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

######################################################################
# Create a new campaign
######################################################################
@login_required
def create_campaign(request):
  if request.method == "POST":
    # Check that all necessary data is present
    cname = request.POST.get("new-camp-name", False)
    gm_pw = request.POST.get("new-camp-gmpw", False)
    pl_pw = request.POST.get("new-camp-pw", False)
    sdesc = request.POST.get("new-camp-sdesc", False)
    if False in (cname, gm_pw, pl_pw, sdesc):
      return HttpResponseBadRequest("Failed to create campaign")
    else:
      success = CampaignManager.add_campaign(request.user, cname, gm_pw, pl_pw, sdesc)
      if success == False:
        return HttpResponseBadRequest("Name conflict")
      else:
        return HttpResponseRedirect(success.name)



######################################################################
# Join on-going campaign
######################################################################
@login_required
def join_campaign(request):
  if request.method == "POST":
    # Check that all necessary data is available
    cname = request.POST.get("join-camp-name", False)
    camppw = request.POST.get("join-camp-pw", False)
    if False in (cname, camppw):
      return HttpResponseBadRequest("Invalid arguments")
    else:
      # CampaignManager knows if password is valid
      success = CampaignManager.join_campaign(request.user, cname, camppw)
      if success:
        return redirect()
      else:
        return HttpResponseBadRequest("Wrong password")
  else:
    HttpResponseBadRequest("Trying some trickstery?")



######################################################################
# Continue on-going campaign
######################################################################
@login_required
def continue_campaign(request, campaign_name):
  # Check that user is participant of the given campaign before redirecting
  if request.user.mycampaigns.filter(name__exact=campaign_name):
    dummy = campaign_name
    return redirect("/campaign_data/" + campaign_name, permanent=True)
    # return redirect(reverse("campaign_data"), args=[campaign_name], permanent=True)
  else:
    return HttpResponseBadRequest("Unable to continue for reason unknown")


# # # # # # # # # # # # # # # #
# CAMPAIGN PAGE FUNCTIONALITY
# # # # # # # # # # # # # # # #

######################################################################
# Campaign data, URL: 'campaign/#name'
######################################################################
@login_required
def campaign_data(request, campaign_name):
  # TODO: Do something and redirect to campaign lobby
  return redirect("/campaign_lobby/" + campaign_name, permanent=True)


######################################################################
# Campaign lobby view TODO: Separate game master and player!
######################################################################
@login_required
def campaign_lobby(request, campaign_name):
  return HttpResponse("You are at campaign lobby")

######################################################################
# Campaign character(s). Regular player see her/his character and
# public NPCs, gamemaster sees everything
######################################################################
@login_required
def character_data(request, character_name):
  pass
