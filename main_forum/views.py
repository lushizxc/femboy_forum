from django.shortcuts import render
from auth_system.models import User
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import Thread, Post
from .forms import PostForm,ThreadForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class DetailUserView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'detail_user.html'

class ThreadListView(ListView):
    model = Thread
    template_name = 'thread_list.html'
    context_object_name = 'threads'
    ordering = ['-created']

class ThreadCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = 'main_forum/thread_form.html'
    success_url = reverse_lazy('main_forum:list')

    def test_func(self):
        return self.request.user.is_moder

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'main_forum/thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all().order_by('created_at')
        return context

class ThreadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Thread
    form_class = ThreadForm
    template_name = 'main_forum/thread_form.html'
    success_url = reverse_lazy('main_forum:list')

    def test_func(self):
        return self.request.user.is_moder

class ThreadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Thread
    template_name = 'main_forum/thread_confirm_delete.html'
    success_url = reverse_lazy('main_forum:list')

    def test_func(self):
        return self.request.user.is_moder

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'main_forum/post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thread_id'] = self.kwargs.get('thread_id')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.thread_id = self.kwargs['thread_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main_forum:thread_detail', kwargs={'pk': self.kwargs['thread_id']})
