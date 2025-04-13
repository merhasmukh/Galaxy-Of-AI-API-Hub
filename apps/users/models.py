from django.db import models

# Create your models here.
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255)  # You can also use ForeignKey if you're using Django's built-in User model
    chat_id = models.CharField(max_length=255)
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