from django.contrib import admin
from .models import users, Photo, PhotoLikes, Followers, PhotoTag
# Register your models here.

admin.site.register(users)
admin.site.register(Photo)
admin.site.register(PhotoLikes)
admin.site.register(Followers)
admin.site.register(PhotoTag)

