from django.urls import path
from .views import PollListView, TakePollView, PollCompleteView,PollCreateView,PollDeleteView,PollStatsView

app_name = 'polls'

urlpatterns = [
    path('polls/', PollListView.as_view(), name='list'),
    path('create/', PollCreateView.as_view(), name='create'), # Создание
    path('<int:poll_id>/delete/', PollDeleteView.as_view(), name='delete'), # Удаление
    path('<int:poll_id>/page/<int:page_number>/', TakePollView.as_view(), name='take_poll'),
    path('<int:poll_id>/complete/', PollCompleteView.as_view(), name='complete'),
    path('<int:poll_id>/stats/', PollStatsView.as_view(), name='stats'),
]