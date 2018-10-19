from django.contrib import admin

from .models import Campaign, AppUser, CampaignParticipant
from .models import Character, MainNPC, SimpleNPC

# Register your models here.
admin.site.register(Campaign)
admin.site.register(AppUser)
admin.site.register(CampaignParticipant)
admin.site.register(Character)
admin.site.register(MainNPC)
admin.site.register(SimpleNPC)
