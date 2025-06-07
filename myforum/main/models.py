from django.db import models
from django.contrib.auth.models import User
    

class ForumPage(models.Model):
    title = models.CharField(max_length=50)
    post = models.TextField(blank=True)
    date_of_post = models.DateTimeField()
    forum_pages = (('І', 'Ігри'), ('К', 'Комп`ютери'), ('П', 'Програмування'), ('Н', 'Новини'))
    forum_choise = models.CharField(choices=forum_pages, default=None)
    
    def __str__(self):
        return self.title
    
    
class Image(models.Model):
    post = models.ForeignKey(ForumPage, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(blank=True)
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usr_comm')
    page = models.ForeignKey(ForumPage, on_delete=models.CASCADE, related_name='comm_pg')
    comment = models.CharField(max_length=255, blank=False)
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='media/user_avatars/')
    
    def __str__(self):
        return self.user