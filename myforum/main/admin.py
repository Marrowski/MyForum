from django.contrib import admin
from .models import ForumPage, Image, Comment, UserProfile

admin.site.register([ForumPage, Image, Comment, UserProfile])

