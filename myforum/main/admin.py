from django.contrib import admin
from .models import ForumPage, Image, Comment

admin.site.register([ForumPage, Image, Comment])

