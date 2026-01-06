from django.db import models
from django.conf import settings

class Poll(models.Model):
    title = models.CharField(max_length=539, verbose_name=" Название опроса")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="Автор")

    def __str__(self):
        return self.title

class Page(models.Model):
    poll = models.ForeignKey(Poll, related_name='pages',on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1, verbose_name="Порядок страницы")
    title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок страницы")

    class Meta:
        ordering = ['order']
        unique_together = ['poll', 'order']

    def __str__(self):
        return f"{self.poll.title} - Страница {self.order}"

    @property
    def has_next(self):
        return Page.objects.filter(poll=self.poll, order__gt=self.order).exists()

class Question(models.Model):
    page = models.ForeignKey(Page, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=400,verbose_name="Вопрос")

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200, verbose_name="Вариант ответа")

    def __str__(self):
        return self.text

class UserResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ответ пользователя"
