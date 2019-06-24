from django.contrib import admin
from .models import Image, Comment, Profile, Contact, Like

admin.site.register(Image)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Like)

