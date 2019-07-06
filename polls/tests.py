import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

#NOTE: Why write test
#Tests save you time
#Tests prevent problems
#Tests make code clearer to other developers:
#   teamwork is much easier
#   open source projects without tests might repel other developers

#also test-driven development is a valid development strategy (see koans)

#NOTE: for tests to work USER from DATABASES settings.py must have
#permission to create databases
class QuestionModelTests(TestCase):
    """Tests for question model"""
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        was more than a day before now
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_questoin(self):
        """
        was_published_recently() returns True for questions whose pub_date
        was less than a day before now
        """
        time = timezone.now() - datetime.timedelta(days=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Create a question with given text, and offset in 'days' days
    Negative 'days' to get past dates
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    """Tests for question index view"""
    def test_no_question(self):
        """
        If no question exist, message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        #check that message is displayed
        self.assertContains(response, "No polls are available")
        #check question list is empty
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Question with a pub_date in the past are displayed on the index page
        """
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

    def test_two_past_question(self):
        """
        Question index page may display more than one question
        """
        create_question(question_text="Past question 1", days=-30)
        create_question(question_text="Past question 2", days=-15)
        response = self.client.get(reverse('polls:index'))
        wanted_result =  ['<Question: Past question 2>', '<Question: Past question 1>']
        self.assertQuerysetEqual(response.context['latest_question_list'], wanted_result)

    def test_future_question(self):
        """
        Question with a pub_date in the furutre are not
        displayed on the index page
        """
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_and_future_question(self):
        """
        If future and past questions exist, only past questions are displayed
        """
        create_question(question_text="Future question", days=30)
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        Future questions should not be in detail list
        (If requested should return error 404)
        """
        future_question = create_question(question_text="Future question", days=5)
        response = self.client.get(reverse("polls:detail",  args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Past question should return status_code 200
        """
        past_question = create_question(question_text="Past question", days=-5)
        response = self.client.get(reverse("polls:detail", args=(past_question.id,)))
        self.assertEqual(response.status_code, 200)