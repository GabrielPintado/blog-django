from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def upload_location(instance, filename):
    return f"media/post_images/{instance.author.username}/{filename}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)

class Post (models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.author_id:  
            if hasattr(self, 'request') and self.request.user.is_authenticated:
                self.author = self.request.user
        super().save(*args, **kwargs) 

class Comment (models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    active= models.BooleanField(default=True)

    def __str__(self):
        return f"comentario de {self.author} {self.content}"
    
    def save(self, *args, **kwargs):
        if not self.author_id:  
            if hasattr(self, 'request') and self.request.user.is_authenticated:
                self.author = self.request.user
        super().save(*args, **kwargs)



class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username} ({self.timestamp})"
    


