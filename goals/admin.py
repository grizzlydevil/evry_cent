from django.contrib import admin

from .models import Goal, Wallet, Pocket, PocketGroup

admin.site.register(Goal)
admin.site.register(Wallet)
admin.site.register(Pocket)
admin.site.register(PocketGroup)
