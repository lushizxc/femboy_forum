from django.urls import path
from main_forum.views import DetailUserView

app_name = 'main_forum'

urlpatterns = [
    path('user/<int:pk>/', DetailUserView.as_view(), name='detail_user'),

]