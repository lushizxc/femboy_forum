from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from .forms import QuestionForm
from .models import Question,Choice,Vote
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView,View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class QuestionListView(ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'voting/question_list.html'

    def get_queryset(self):
        return Question.objects.filter(status='active')


class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'voting/question_detail.html'

class VoteView(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        question = get_object_or_404(Question, pk=pk)
        try:
            selected_choice_id = request.POST['choice']
            selected_choice = get_object_or_404(Choice,pk=selected_choice_id)

        except(KeyError, Choice.DoesNotExist):
            return render(request,'voting/question_detail.html',{
                'question': question,
                'error_message': "Вы не выбрали вариант ответа.",
            })


        else:
            Vote.objects.update_or_create(question=question,who_voted=request.user,defaults={'choice':selected_choice})


        return redirect('voting:results',pk=question.pk)


class QuestionCreationView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Question
    template_name = 'voting/question_form.html'
    success_url = reverse_lazy('voting:question_list')
    form_class = QuestionForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        options_text = form.cleaned_data['options']

        for line in options_text.splitlines():
            if line.strip():
                Choice.objects.create(
                    question=self.object,
                    content=line.strip()
                )

        return response

    def test_func(self):
        return self.request.user.is_moder() or self.request.user.is_admin()

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    template_name = 'voting/question_form.html'
    success_url = reverse_lazy('voting:question_list')

    form_class = QuestionForm

    def test_func(self):
        return self.request.user.is_moder or self.request.user.is_admin()

class QuestionDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Question
    template_name = 'voting/question_delete_confirm.html'
    success_url = reverse_lazy('voting:question_list')


    def test_func(self):
        return self.request.user.is_moder() or self.request.user.is_admin()


class QuestionInactiveConfirmationView(LoginRequiredMixin,UserPassesTestMixin,View):
    def post(self,request,pk):
        question = get_object_or_404(Question, pk=pk)
        question.status = 'closed'
        question.save()
        return redirect('voting:question_list')


    def test_func(self):
        return self.request.user.is_moder() or self.request.user.is_admin()


class ResultsView(DetailView):
    model = Question
    template_name = 'voting/results.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.object
        total_votes = question.vote_set.count()
        choices_data = []

        for choice in question.choices.all():
            votes = choice.vote_set.all()
            percent = (votes.count() / total_votes * 100) if votes.count() > 0 else 0

            choices_data.append({
                'choice': choice,
                'percent': percent,
                'total_votes': round(percent,1)
            })

            context['choices_data'] = choices_data
            context['total_votes'] = total_votes
            return context
