from django.contrib import admin

# Register your models here.

from .models import RegisteredUser, Airdrops, Step,BlogPost
admin.site.register(RegisteredUser)
admin.site.register(Airdrops)
admin.site.register(Step)
admin.site.register(BlogPost)