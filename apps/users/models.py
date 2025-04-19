from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()# Create your models here.
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    chat_id = models.CharField(max_length=255)
    name = models.CharField(max_length=50,default="AI Assistant") 
    description = models.TextField(default="AI Research")
    language = models.CharField(max_length=50,default="english")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.chat_id


class ChatMessages(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat_id

class ResourceManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    url = models.URLField()
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    


class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.description[:30]}"



class Projects(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title