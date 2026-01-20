from django.urls import path
from .views import QuestionListView,QuestionDetailView,VoteView,ResultsView,QuestionDeleteView,QuestionUpdateView,QuestionCreationView,QuestionInactiveConfirmationView

app_name = 'voting'

urlpatterns = [
    path('/q_list', QuestionListView.as_view(), name='question_list'),
    path('<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('<int:pk>/vote/', VoteView.as_view(), name='vote'),
    path('<int:pk>/results/', ResultsView.as_view(), name='results'),
    path('/create',QuestionCreationView.as_view(), name='question_create'),
    path('<int:pk>/delete',QuestionDeleteView.as_view(), name='question_delete'),
    path('<int:pk>/update',QuestionUpdateView.as_view(), name='question_update'),
    path('<int:pk>/inactive',QuestionInactiveConfirmationView.as_view(), name='inactive'),
]