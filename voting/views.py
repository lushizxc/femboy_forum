from django.shortcuts import get_object_or_404, render, redirect
from .models import Question,Choice,Vote
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView,View
from django.contrib.auth.mixins import LoginRequiredMixin

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

class VoteView(View,LoginRequiredMixin):
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
            Vote.objects.update_or_create(question=question,choice=selected_choice,who_voted=request.user)

        return redirect('results',pk=question.pk)
