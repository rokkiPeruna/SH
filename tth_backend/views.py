from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
# To prevent unauthorized access to views
from django.contrib.auth.decorators import login_required

# Models
from .models import Campaign

######################################################################
# First place to land, the index which directs directly to login page.
# Login view is from Django, login.html is in root/registration/login.html
######################################################################
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
    "campaigns": Campaign.objects.all()
  }
  return render(request, "main.html", response)


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
    name = request.POST.get("new-camp-name")
    pl_pw = request.POST.get("new-camp-pw")
    gm_pw = request.POST.get("new-camp-gmpw")
    sdesc = request.POST.get("name")

  pass


######################################################################
# Join on-going campaign
######################################################################
@login_required
def join_campaign(request):
  pass

######################################################################
# Continue on-going campaign
######################################################################
@login_required
def continue_campaign(request):
  pass


# # # # # # # # # # # # # # # #
# CAMPAIGN PAGE FUNCTIONALITY
# # # # # # # # # # # # # # # #

# TODO: Ensure that only campaign's players can see these views

######################################################################
# Campaign data, URL: 'campaign/#name'
######################################################################
def campaign_data(request, campaign_name):
  pass


######################################################################
# Campaign character(s). Regular player see her/his character and
# public NPCs, gamemaster sees everything
######################################################################
def character_data(request, character_name):
  pass
