from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404

# How large character datasheet can get
DATASHEET_MAX_LENGTH = 65535 #64 kB, should be enough for normal writers

# Campaign roles
PLAYER = "PL"
GAMEMASTER = "GM"
SPECTATOR = "SPEC"
ROLES = (
  (PLAYER, "Player"),
  (GAMEMASTER, "GameMaster"),
  (SPECTATOR, "Spectator")
)

# Logic: Campaigns are the umbrellas that gather everything else under
# them: Users can join and leave campaigns and characters can born and die under
# campaigns. Each campaign can have multiple players and at least one game master.
# By authenticating, user gains access to her/his characters but campaigns come
# available only if campaign password is known. Characters are bound to the campaign
# and can't leave and join other campaigns unless the campaign they are bound to
# is either terminated or the character dies. Each character holds a character
# sheet which is their main source of information.
# Users are bound to the campaign via their character and password.



######################################################################
# CampaignManager handles campaign operations that involve the modification
# of the Campaign-database table, not a single campaign instance.
# Returns False if conflict, campaign model otherwise
######################################################################
class CampaignManager(models.Manager):

  # Add campaign to database if no name conflicts. Adds creator as the game master.
  # On failure returns False and error message.
  # On success returns the campaign.
  def add_campaign(user, camp_name, gmpw, plpw, sdesc):
    try: #to find existing campaign
      Campaign.objects.get(name__exact=camp_name)
    except Campaign.DoesNotExist as success: #No such campaign exists!
      campaign = Campaign.objects.create(name=camp_name, gmpassword=gmpw, playerpassword=plpw, shortdescription=sdesc)
      user.campaigns.add(campaign)
      return campaign, "Successfully created campaing!"
    except models.MultipleObjectsReturned as err:
      # Something is terribly wrong
      return False, "Multiple campaigns with name {} exists!".format(camp_name)
    else:
      return False, "Internal error when adding campaign"


  # Adds user to campaign if campaign with given name exists and password matches.
  # Returns False and error message if joining fails or campaign doesn't exist.
  # Returns True and campaign model on successful join.
  def join_campaign(user, camp_name, cpw):
    try:
      campaign = Campaign.objects.get(name__exact=camp_name)
      if campaign.playerpassword == cpw:
        user.campaigns.add(campaign)
        return True, campaign
      else:
        return False, "Password didn't match"
    except (Campaign.MultipleObjectsReturned, Campaign.DoesNotExist) as err:
      # TODO: Log properly
      return False, "No campaign with that name"

  # Get campaign by name. Returns campaign model on success, False on failure
  def get_campaign_by_name(camp_name):
    # Check that campaign exists
    try:
      campaign = Campaign.objects.get(name__exact=camp_name)
      return campaign
    except Campaign.MultipleObjectsReturned as err:
      # TODO: Log properly
      return False
    except Campaign.DoesNotExist as err:
      # TODO: Log properly
      return False

  # Remove campaign from database (only game master is authorized)
  def remove_campaign(camp_name):
    pass

######################################################################
# Campaign represents a tabletop game which has a game master(s)
# and players.
######################################################################
class Campaign(models.Model):
  # Story/campaign name
  name = models.CharField(max_length=100)
  # For joining as game master
  gmpassword = models.CharField(max_length=100)
  # For joining as player
  playerpassword = models.CharField(max_length=100)
  # Shown at main lobby
  shortdescription = models.CharField(max_length=150)
  # Story this far
  story = models.TextField(max_length=DATASHEET_MAX_LENGTH)
  # Maps ?
  # Simple character store ?
  # More ... ?

  objects = CampaignManager()

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return "/campaign/%s" % self.name


######################################################################
# User represents application user. Application user can join many
# game campaigns, be either game master or player in those campaigns and
# have several different characters.
# User inherits from AbstractUser so it works also as the authentication
# model.
######################################################################
class User(AbstractUser):
  # App users can join many campaigns and campaigns can have many user
  campaigns = models.ManyToManyField(Campaign)
  # Created
  created = models.DateField(auto_now_add=True)
  # Last saved
  last_saved = models.DateField(auto_now=True)

  def __str__(self):
    return self.usr_name


######################################################################
# Handles operations made to multiple Character models
######################################################################
class CharacterManager(models.Manager):
  # Returns campaigns all character models as queryset (NOTE: for GM only)
  def get_campaign_characters(camp_name):
      return None

  # Creates character and binds it to given user
  def create_character(user, name):
    Character.objects.create(
      user=user,
      name=name,
      datasheet="{data: dummy data}"
    )

  # Returns all user's characters
  def get_user_characters(user):
    return Character.objects.filter(user_id=user.id)

  # Deletes character
  def delete_character(name):
    pass

  # Saves character with new datasheet
  def save_character(name, datasheet):
    pass


######################################################################
# Character represents a character in a game campaign.
######################################################################
class Character(models.Model):
  # Each normal character is bound to a single user
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # Character name
  name = models.CharField(max_length=100)
  # Character's data sheet as JSON
  datasheet = models.TextField(max_length=DATASHEET_MAX_LENGTH)
  # Created
  created = models.DateField(auto_now_add=True)
  # Last saved
  last_saved = models.DateField(auto_now=True)
  # Custom manager
  objects = CharacterManager()

  def __str__(self):
    return self.name


######################################################################
# MainNPC represents an NPC which is key part of the campaign.
######################################################################
class MainNPC(models.Model):
  # Each main NPC is bound to a single campaign
  campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
  # Actual name as in 'John the Dripper'
  name = models.CharField(max_length=100)
  # NPC data sheet in JSON
  datasheet = models.TextField(max_length=DATASHEET_MAX_LENGTH)
  # Is NPC's data visible to players?
  is_public = models.BooleanField(default=False)
  # Created
  created = models.DateField(auto_now_add=True)
  # Last saved
  last_saved = models.DateField(auto_now=True)

  def __str__(self):
    return self.name


######################################################################
# SimpleNPC represents a simple NPC which can used in small, quite
# meaningless encounters, such as bar brawls or as passing quards etc.
######################################################################
class SimpleNPC(models.Model):
  name = models.CharField(max_length=100)
  # Each simple NPC is bound to a single campaign
  campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
  # NPC data sheet in JSON
  datasheet = models.TextField(max_length=DATASHEET_MAX_LENGTH)
  # Is simple NPC's data visible to players?
  is_public = models.BooleanField(default=False)
  # Created
  created = models.DateField(auto_now_add=True)
  # Last saved
  last_saved = models.DateField(auto_now=True)

  def __str__(self):
    return self.name
