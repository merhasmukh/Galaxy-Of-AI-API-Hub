from django.db import models

# Create your models here.
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255)  # You can also use ForeignKey if you're using Django's built-in User model
    chat_id = models.CharField(max_length=255)
    name = models.CharField(max_length=50,default="AI Research Assistant") 
    description = models.TextField(default="Project description")
    language = models.CharField(max_length=50,default="english")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat_id


class ChatMessages(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat_id

class ResourceManager(models.Model):
    RESOURCE_TYPES = (
        ('url', 'General URL'),
        ('blog', 'Blog URL'),
    )

    title = models.CharField(max_length=255)
    url = models.URLField()
    type = models.CharField(max_length=10, choices=RESOURCE_TYPES)

    def __str__(self):
        return self.title