from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice, Comment

class IndexView(generic.ListView):
    #override default template name <app name>/<model name>_list.html
    #default:polls/Question_list
    template_name = 'polls/index.html'
    #override default object name <object>_list
    #default: question_list
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the las five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    #model name, duh
    model = Question
    #override default template name <app name>/<model name>_detail.html
    #default name: polls/question_detail.html
    template_name = 'polls/detail.html'

class CommentsView(generic.DetailView):
    model = Question
    template_name = 'polls/comments.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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
    # return HttpResponse("You're voiting on question %s" % question_id)