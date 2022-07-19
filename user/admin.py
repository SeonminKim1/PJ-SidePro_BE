from django.contrib import admin
from .models import User
from .models import MeetTime
from .models import Region
from .models import Skills
from .models import UserProfile


admin.site.register(User)
admin.site.register(MeetTime)
admin.site.register(Region)
admin.site.register(Skills)
admin.site.register(UserProfile)