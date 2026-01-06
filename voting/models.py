from django.db import models
from auth_system.models import User

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('active', 'active'),
        ('closed', 'closed'),
    ]

    status = models.CharField(max_length=10, default='active', choices=STATUS_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='choices')
    content = models.TextField()

    def __str__(self):
        return self.content


class Vote(models.Model):
    who_voted = models.ForeignKey(User, on_delete=models.CASCADE,related_name='votes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('who_voted','question')

    def __str__(self):
        return f"{self.who_voted} -> {self.choice}"