from django.urls import path
from .views import QuestionListView,QuestionDetailView,VoteView

app_name = 'voting'

urlpatterns = [
    path('qlist/', QuestionListView.as_view(), name='question_list'),
    path('qdetail/', QuestionDetailView.as_view(), name='question_detail'),
    path('<int:pk>/vote/', VoteView.as_view(), name='vote'),
]