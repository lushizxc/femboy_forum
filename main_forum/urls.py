from django.urls import path
from main_forum.views import (DetailUserView,ThreadListView,ThreadCreateView,ThreadDetailView,
                              PostCreateView,ThreadDeleteView,ThreadUpdateView,IndexView,AdminUserRoleEditView)

app_name = 'main_forum'

urlpatterns = [
    path('user/<int:pk>/', DetailUserView.as_view(), name='detail_user'),
    path('forum/', ThreadListView.as_view(), name='list'),
    path('thread/create/', ThreadCreateView.as_view(), name='thread_create'),
    path('thread/<int:pk>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('thread/<int:thread_id>/add-post/', PostCreateView.as_view(), name='post_add'),
    path('thread/<int:pk>/edit/', ThreadUpdateView.as_view(), name='thread_edit'),
    path('thread/<int:pk>/delete/', ThreadDeleteView.as_view(), name='thread_delete'),
    path('user/<int:pk>/change-role/', AdminUserRoleEditView.as_view(), name='change_role'),
    path('', IndexView.as_view(), name='index'),
]