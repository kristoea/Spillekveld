from django.contrib import admin

from .models import Organizer, Event, Signup

admin.site.register(Event)
admin.site.register(Organizer)
admin.site.register(Signup)

