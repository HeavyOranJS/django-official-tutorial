from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Count

from .models import Question, Choice, Comment

class IndexView(generic.ListView):
    #override default template name <app name>/<model name>_list.html
    #default:polls/Question_list
    template_name = 'polls/index.html'
    #override default object name <object>_list
    #default: question_list
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Returns the last five published questions.
        """
        now = timezone.now()
        return Question.objects.filter(pub_date__lte=now).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    #model name, duh
    model = Question
    #override default template name <app name>/<model name>_detail.html
    #default name: polls/question_detail.html
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Returns questions with publishing date older than now.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Returns all questions with at least 1 choice.
        """
        return Question.objects.annotate(num_choice=Count('choice')).filter(num_choice__gt=0)

class CommentsView(generic.DetailView):
    model = Question
    template_name = 'polls/comments.html'

    def get_queryset(self):
        """
        Returns all questions with at least 1 comment.
        """
        return Question.objects.annotate(num_comment=Count('comment')).filter(num_comment__gt=0)

def leave_comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #get comment_text and is comment positive from post request
    #with kwarg(keyword arg) comment_text
    comment = Comment(
            question=question,
            comment_text=request.POST['comment_text'],
            positive=request.POST['is_positive']
        )
    comment.save()
    return HttpResponseRedirect(reverse('polls:comments', args=(question_id,)))

def vote(request, question_id):
    #get question or 404 
    #if there is no question with this PK
    question = get_object_or_404(Question, pk=question_id)
    try:
        #get selected string choice by PK from post request
        #with kwarg(keyword arg) choice
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #if there is no choice with this PK
        #return to detail page with error message
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message': "You didn't select a choice",
        })
    else:
        #if everything is fine add vote and save choice
        selected_choice.votes += 1
        selected_choice.save()
        # "Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button." by docs.djangoproject.com
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        #TODO why do i need reverse and cant write like this
        # return HttpResponse('polls:results', args=(question.id,))