from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Campaign, User
from .models import Character, MainNPC, SimpleNPC

# Register your models here.
admin.site.register(Campaign)
admin.site.register(User, UserAdmin)
admin.site.register(Character)
admin.site.register(MainNPC)
admin.site.register(SimpleNPC)
