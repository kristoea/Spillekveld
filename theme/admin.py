from django.contrib import admin

from .models import Organizer, Event

admin.site.register(Event)
admin.site.register(Organizer)
