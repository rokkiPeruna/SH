from django.db import models
from django.contrib.auth.models import AbstractUser

# How large character datasheet can get
DATASHEET_MAX_LENGTH = 65535 #64 kB, should be enough for normal writers

# Campaign participant roles
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
# Session participant model is used as intermediary when
# handling campaign roles and data.


######################################################################
# CampaignManager handles campaign operations that involve the modification
# of the Campaign-database table, not a single campaign instance.
# Returns False if conflict, campaign model otherwise
######################################################################
class CampaignManager(models.Manager):

  # Add campaign to database if no name conflicts. Adds creator as participant
  # with game master role.
  # Returns False if campaign with given name exists.
  # On successful creation the campaign model is returned
  def add_campaign(user, cname, gmpw, plpw, sdesc):
    if Campaign.objects.filter(name=cname):
      return False
    else:
      # Create campaign,
      campaign = Campaign.objects.create(name=cname, gmpassword=gmpw, playerpassword=plpw, shortdescription=sdesc)
      # add user to the campaign
      user.mycampaigns.add(campaign)
      # and create participant with game master role that is bound to the user
      # and the campaign
      partic = CampaignParticipantManager.create_and_bind_participant(user, campaign, GAMEMASTER)
      return campaign

  # Adds user to campaign is campaign with given name exists and password matches.
  # Returns False and error message if joining fails or campaign doesn't exist.
  # Returns True and campaign model on successful join.
  def join_campaign(user, cname, cpw):
    # Check that campaign exists
    if Campaign.objects.filter(name__exact=cname):
      # Get first (and only) campaign from query set
      campaign = Campaign.objects.filter(name__exact=cname)[0]
      # Match password
      if campaign.playerpassword == cpw:
        # Add campaign to user
        user.mycampaigns.add(campaign)
        # and create and bind participant model
        partic = CampaignParticipantManager.create_and_bind_participant(user, campaign, PLAYER)
        return True, campaign
      else: # return with error
        return False, "Password didn't match"
    else:
      return False, "No campaign with that name"

  # Get campaign by name. Returns campaign model on success, False on failure
  def get_campaign_by_name(cname):
    # Check that campaign exists
    if Campaign.objects.filter(name__exact=cname):
      # Get first (and only) campaign from query set
      campaign = Campaign.objects.filter(name__exact=cname)[0]
      return campaign
    else:
      return False

  # Remove campaign from database (only game master is authorized)
  def remove_campaign(cname):
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
  mycampaigns = models.ManyToManyField(Campaign)
  # Created
  created = models.DateField(auto_now_add=True)
  # Last saved
  last_saved = models.DateField(auto_now=True)

  def __str__(self):
    return self.username


######################################################################
# CampaignParticipantManager handles bindings between users and campaigns
# via the CampaignParticipant model
######################################################################
class CampaignParticipantManager(models.Manager):
  # Creates participant and binds it to given user and campaign with given role.
  # Returns the created participant.
  def create_and_bind_participant(user, campaign, role):
    partic = CampaignParticipant.objects.create(owner=user, campaign=campaign, name=user.username, role=role)
    return partic

  def delete_participant(user):
    pass

######################################################################
# CampaignParticipant represents the game campaign's player or game master
######################################################################
class CampaignParticipant(models.Model):
  # Each campaign participant is bound to single campaign
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  # and to a single user
  campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
  # Name of the participant, gets set to User's username
  name = models.CharField(max_length=100)
  # Role: either player or game master (or spectator)
  role = models.CharField(
    max_length=4,
    choices=ROLES,
    default=PLAYER
  )
  # Notes about the campaign
  campaign_notes = models.TextField(max_length=(DATASHEET_MAX_LENGTH/2))
  # Created
  created = models.DateField(auto_now_add=True)
  # Last saved
  last_saved = models.DateField(auto_now=True)

  # Custom manager
  objects = CampaignParticipantManager()

  def is_gamemaster(self):
    return (self.role == GAMEMASTER)

  def __str__(self):
    return self.name


######################################################################
# Handles operations made to multiple Character models
######################################################################
class CharacterManager(models.Manager):
  # Returns campaigns all character models as queryset (NOTE: for GM only)
  def get_campaign_characters(campaign):
    return Character.objects.get(id=campaign_id)

  # Creates character and binds it to given participant
  def create_character(participant, name):
    Character.objects.create(
      participant=participant,
      name=name,
      datasheet="{data: dummy data}"
    )

  # Deletes character and unbinds it from owner participant
  def delete_character(name):
    pass

  # Saves character with new datasheet
  def save_character(name, datasheet):
    pass


######################################################################
# Character represents a character in a game campaign. It can be a user's
# character or an NPC created by the game master(s).
######################################################################
class Character(models.Model):
  # Each normal character is bound to single campaign participant
  participant = models.ForeignKey(CampaignParticipant, on_delete=models.CASCADE)
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
  name = models.CharField(max_length=100)
  # Each main NPC is bound to a single campaign
  campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
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
