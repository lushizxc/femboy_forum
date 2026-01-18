from django.shortcuts import render
from auth_system.models import User
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView,TemplateView
from .models import Thread, Post
from .forms import PostForm,ThreadForm,UserRoleForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from itertools import chain
from polls.models import Poll
from voting.models import Question as VotingQuestion

class DetailUserView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'main_forum/detail_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = self.object


        context['user_threads'] = target_user.thread_set.all().order_by('-created')
        context['user_polls'] = target_user.poll_set.all().order_by('-created_at')
        context['user_questions'] = target_user.question_set.all().order_by('-date')

        return context
class ThreadListView(ListView):
    model = Thread
    template_name = 'thread_list.html'
    context_object_name = 'threads'
    ordering = ['-created']

class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = 'main_forum/thread_form.html'
    success_url = reverse_lazy('main_forum:list')


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

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        threads = Thread.objects.all().order_by('-created')
        polls = Poll.objects.all().order_by('-created_at')
        voting_qs = VotingQuestion.objects.filter(status='active').order_by('-date')

        for t in threads:
            t.content_type = 'thread'
        for p in polls:
            p.content_type = 'poll'
        for v in voting_qs:
            v.content_type = 'vote'

        def get_date(obj):
            if hasattr(obj, 'created'): return obj.created
            if hasattr(obj, 'created_at'): return obj.created_at
            return obj.date

        combined_feed = sorted(
            chain(threads, polls, voting_qs),
            key=get_date,
            reverse=True
        )

        context['feed_items'] = combined_feed[:30]
        return context


class AdminUserRoleEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserRoleForm
    template_name = 'auth_system/admin_role_edit.html'

    def get_success_url(self):
        return reverse_lazy('main_forum:detail_user', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.is_moder() or self.request.user.is_admin()
