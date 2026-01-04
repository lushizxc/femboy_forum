from django.db import models
from django.conf import settings

class Thread(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название темы")
    description = models.TextField(blank=True,verbose_name="Описание")
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE,related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author} in {self.thread.title}"

    