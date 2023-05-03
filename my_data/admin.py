from django.contrib import admin
from .models import *
# Register your models here.
model = [Project, Activity, Event, Participants, Actions, Province, District, Palika]

admin.site.register(model)