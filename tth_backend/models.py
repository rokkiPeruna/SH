from django.db import models

# How large character datasheet can get
DATASHEET_MAX_LENGTH = 65535 #64 kB, should be enough for normal writers


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
# Campaign represents a tabletop game which has a game master(s)
# and players.
######################################################################
class Campaign(models.Model):
  name = models.CharField(max_length=100)   # Story/campaign name
  passwd = models.CharField(max_length=100) # For joining the campaign

  # Story ?
  # Maps ?
  # Simple character store ?
  # More ... ?


  def __str__(self):
    return self.name

######################################################################
# AppUser represents application user. Application user can join many
# game campaigns, be either game master or player in those campaigns and
# have several different characters.
######################################################################
class AppUser(models.Model):
  name = models.CharField(max_length=30)  # Actual human name
  alias = models.CharField(max_length=30) # Human's nickname
  # Created
  created = models.DateField(auto_now_add=True)
  # Last saved
  last_saved = models.DateField(auto_now=True)


  def __str__(self):
    return self.name


######################################################################
# SessionParticipant represents the game campaign's player or a master
######################################################################
class SessionParticipant(models.Model):
  name = models.CharField(max_length=100)
  # Role: either player or game master (or spectator)
  PLAYER = "PL"
  GAMEMASTER = "GM"
  SPECTATOR = "SPEC"
  ROLES = (
    (PLAYER, "Player"),
    (GAMEMASTER, "GameMaster"),
    (SPECTATOR, "Spectator")
  )
  role = models.CharField(
    max_length=4,
    choices=ROLES,
    default=PLAYER
  )
  # Each campaign participant is bound to single campaign
  campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
  # Created
  created = models.DateField(auto_now_add=True)
  # Last saved
  last_saved = models.DateField(auto_now=True)

  def is_gamemaster(self):
    return (self.role == GAMEMASTER)

  def __str__(self):
    return self.name


######################################################################
# Character represents a character in a game campaign. It can be a user's
# character or an NPC created by the game master(s).
######################################################################
class Character(models.Model):
  name = models.CharField(max_length=100)
  # Each normal character is bound to single campaign participant
  participant = models.ForeignKey(SessionParticipant)
  # Character's data sheet as JSON
  datasheet = models.TextField(max_length=DATASHEET_MAX_LENGTH)
  # Created
  created = models.DateField(auto_now_add=True)
  # Last saved
  last_saved = models.DateField(auto_now=True)

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
