from django.shortcuts import render
from auth_system.models import User
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView


class DetailUserView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'detail_user.html'

