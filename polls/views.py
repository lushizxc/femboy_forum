from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Poll, Page, Choice, UserResponse,Question
from django.core.paginator import Paginator
from django.db.models import Count



class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff



class PollListView(View):

    def get(self, request):
        polls_list = Poll.objects.all().order_by('-created_at')
        paginator = Paginator(polls_list, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'polls/list.html', {'page_obj': page_obj})

class TakePollView(LoginRequiredMixin, View):
    def get(self, request, poll_id, page_number):
        poll = get_object_or_404(Poll, id=poll_id)
        page = get_object_or_404(Page, poll=poll, order=page_number)

        if page_number == 1:
            if 'poll_data' not in request.session:
                request.session['poll_data'] = {}
            request.session['poll_data'][str(poll_id)] = {}
            request.session.modified = True

        return render(request, 'polls/take_poll.html', {'poll': poll, 'page': page})

    def post(self, request, poll_id, page_number):
        poll = get_object_or_404(Poll, id=poll_id)
        page = get_object_or_404(Page, poll=poll, order=page_number)


        poll_data = request.session.get('poll_data', {})
        if str(poll_id) not in poll_data:
            poll_data[str(poll_id)] = {}

        for question in page.questions.all():
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                poll_data[str(poll_id)][str(question.id)] = choice_id

        request.session['poll_data'] = poll_data
        request.session.modified = True

        next_page = Page.objects.filter(poll=poll, order__gt=page_number).first()
        if next_page:
            return redirect('polls:take_poll', poll_id=poll.id, page_number=next_page.order)

        return self.save_results(request, poll)

    def save_results(self, request, poll):
        poll_data = request.session.get('poll_data', {}).get(str(poll.id), {})

        UserResponse.objects.filter(user=request.user, poll=poll).delete()

        responses = []
        for q_id, c_id in poll_data.items():
            responses.append(UserResponse(
                user=request.user,
                poll=poll,
                choice_id=int(c_id)
            ))
        UserResponse.objects.bulk_create(responses)

        del request.session['poll_data'][str(poll.id)]
        request.session.modified = True

        return redirect('polls:complete', poll_id=poll.id)

class PollCompleteView(LoginRequiredMixin, View):
    def get(self, request, poll_id):
        return render(request, 'polls/complete.html', {'poll_id': poll_id})

class PollCreateView(StaffRequiredMixin, CreateView):
    model = Poll
    fields = ['title', 'description']
    template_name = 'polls/poll_form.html'
    success_url = reverse_lazy('polls:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PollDeleteView(StaffRequiredMixin, DeleteView):
    model = Poll
    template_name = 'polls/poll_confirm_delete.html'
    success_url = reverse_lazy('polls:list')
    pk_url_kwarg = 'poll_id'

class PollStatsView(LoginRequiredMixin, View):
    def get(self, request, poll_id):
        if not request.user.is_staff:
            return redirect('polls:list')

        poll = get_object_or_404(Poll, id=poll_id)
        questions = Question.objects.filter(page__poll=poll)

        stats = []
        for q in questions:
            choices = q.choices.annotate(num_responses=Count('userresponse'))
            total_for_question = sum(c.num_responses for c in choices)

            for c in choices:
                c.percentage = (c.num_responses / total_for_question * 100) if total_for_question > 0 else 0

            stats.append({
                'question': q.text,
                'choices': choices
            })

        return render(request, 'polls/stats.html', {'poll': poll, 'stats': stats})