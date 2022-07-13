from django.contrib import admin
from .models import User, MeetTime, Region, Skills, UserProfile
# Register your models here.

admin.site.register(User)
admin.site.register(MeetTime)
admin.site.register(Region)
admin.site.register(Skills)
admin.site.register(UserProfile)