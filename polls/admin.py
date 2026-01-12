from django.contrib import admin
from .models import Poll, Page, Question, Choice, UserResponse

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('poll', 'order', 'title')
    list_filter = ('poll',)
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'page')
    inlines = [ChoiceInline]

@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'poll', 'choice', 'created_at')
    readonly_fields = ('user', 'poll', 'choice', 'created_at')

admin.site.register(Poll)