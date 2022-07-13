from django.contrib import admin

from .models import Status
from .models import Room
from .models import Chat

# Register your models here.
admin.site.register(Status)
admin.site.register(Room)
admin.site.register(Chat)