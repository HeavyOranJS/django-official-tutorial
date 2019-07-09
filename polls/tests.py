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
def create_question(question_text, days):
    """
    Create a question with given text, and offset in 'days' days
    Negative 'days' to get past dates
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

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

    #count_comment tests
    def test_count_comments_no_comments(self):
        """
        сount_comments() returns 0 if question has no comments
        """
        question_without_comments = create_question(question_text="Question with responce", days=1)
        comment_amount = question_without_comments.count_comments()
        self.assertEqual(comment_amount, 0)

    def test_count_comments_1_comment(self):
        """
        сount_comments() returns 1 if question has 1 comment
        """
        question_with_comments = create_question(question_text="Question with responce", days=1)
        question_with_comments.comment_set.create(comment_text='Voted comment', positive=True)
        comment_amount = question_with_comments.count_comments()
        self.assertEqual(comment_amount, 1)

    def test_count_comments_multiple_comments(self):
        """
        сount_comments() returns 21 if question has 2 comments
        """
        question_with_comments = create_question(question_text="Question with responce", days=1)
        question_with_comments.comment_set.create(comment_text='Voted comment', positive=True)
        question_with_comments.comment_set.create(comment_text='Other comment', positive=True)
        comment_amount = question_with_comments.count_comments()
        self.assertEqual(comment_amount, 2)

    #count_coments_positive tests
    def test_count_comments_positive_positive_no_comments(self):
        """
        сount_comments() returns 0 if question has no comments
        """
        question_without_comments = create_question(question_text="Question with responce", days=1)
        positive_comment_amount = question_without_comments.count_comments_positive()
        self.assertEqual(positive_comment_amount, 0)

    def test_count_comments_positive_positive_comment(self):
        """
        сount_comments() returns 1 if question has 1 positive comment
        """
        question_with_comments = create_question(question_text="Question with responce", days=1)
        question_with_comments.comment_set.create(comment_text='Voted comment', positive=True)
        positive_comment_amount = question_with_comments.count_comments_positive()
        self.assertEqual(positive_comment_amount, 1)

    def test_count_comments_positive_multiple_positive_comments(self):
        """
        сount_comments() returns 2 if question has 2 positive comments
        """
        question_with_comments = create_question(question_text="Question with responce", days=1)
        question_with_comments.comment_set.create(comment_text='Voted comment', positive=True)
        question_with_comments.comment_set.create(comment_text='Other comment', positive=True)
        positive_comment_amount = question_with_comments.count_comments_positive()
        self.assertEqual(positive_comment_amount, 2)

    def test_count_comments_positive_multiple_positive_comments_and_negative_comment(self):
        """
        сount_comments() returns 2 if question has 2 positive comments and doesnt get triggered
        by negative one
        """
        question_with_comments = create_question(question_text="Question with responce", days=1)
        question_with_comments.comment_set.create(comment_text='Voted comment', positive=True)
        question_with_comments.comment_set.create(comment_text='Other comment', positive=True)
        question_with_comments.comment_set.create(comment_text='Negative comment', positive=False)
        positive_comment_amount = question_with_comments.count_comments_positive()
        self.assertEqual(positive_comment_amount, 2)

    def test_count_comments_positive_negative_comment(self):
        """
        сount_comments() doesnt get triggered by negative comment
        """
        question_with_comments = create_question(question_text="Question with responce", days=1)
        question_with_comments.comment_set.create(comment_text='Voted comment', positive=False)
        positive_comment_amount = question_with_comments.count_comments_positive()
        self.assertEqual(positive_comment_amount, 0)

    def test_count_comments_positive_multiple_negative_comments(self):
        """
        сount_comments() doesnt get triggered by multiple negative comments
        """
        question_with_comments = create_question(question_text="Question with responce", days=1)
        question_with_comments.comment_set.create(comment_text='Voted comment', positive=False)
        question_with_comments.comment_set.create(comment_text='Other comment', positive=False)
        positive_comment_amount = question_with_comments.count_comments_positive()
        self.assertEqual(positive_comment_amount, 0)
    
    def test_count_comments_positive_multiple_negative_comments_and_positive_comment(self):
        """
        сount_comments() returns 1 if question has a positive comment and doesnt get triggered
        by negative ones
        """
        question_with_comments = create_question(question_text="Question with responce", days=1)
        question_with_comments.comment_set.create(comment_text='Negative comment', positive=False)
        question_with_comments.comment_set.create(comment_text='Other negative comment', positive=False)
        question_with_comments.comment_set.create(comment_text='Postive comment', positive=True)
        positive_comment_amount = question_with_comments.count_comments_positive()
        self.assertEqual(positive_comment_amount, 1)
    
    def test_count_comments_positive_multiple_negative_and_positive_comments(self):
        """
        сount_comments() returns 2 if question has 2 positive comments and doesnt get triggered
        by negative ones
        """
        question_with_comments = create_question(question_text="Question with responce", days=1)
        question_with_comments.comment_set.create(comment_text='Negative comment', positive=False)
        question_with_comments.comment_set.create(comment_text='Other negative comment', positive=False)
        question_with_comments.comment_set.create(comment_text='Postive comment', positive=True)
        question_with_comments.comment_set.create(comment_text='Other postive comment', positive=True)
        positive_comment_amount = question_with_comments.count_comments_positive()
        self.assertEqual(positive_comment_amount, 2)

    #count_coments_negative tests
    def test_count_comments_negative_negative_no_comments(self):
        """
        сount_comments() returns 0 if question has no comments
        """
        question_without_comments = create_question(question_text="", days=1)
        positive_comment_amount = question_without_comments.count_comments_negative()
        self.assertEqual(positive_comment_amount, 0)

    def test_count_comments_negative_negative_comment(self):
        """
        сount_comments() returns 1 if question has 1 negative comment
        """
        question_with_comments = create_question(question_text="", days=1)
        question_with_comments.comment_set.create(comment_text='', positive=False)
        positive_comment_amount = question_with_comments.count_comments_negative()
        self.assertEqual(positive_comment_amount, 1)

    def test_count_comments_negative_multiple_negative_comments(self):
        """
        сount_comments() returns 2 if question has 2 negative comments
        """
        question_with_comments = create_question(question_text="", days=1)
        question_with_comments.comment_set.create(comment_text='', positive=False)
        question_with_comments.comment_set.create(comment_text='', positive=False)
        positive_comment_amount = question_with_comments.count_comments_negative()
        self.assertEqual(positive_comment_amount, 2)

    def test_count_comments_negative_multiple_negative_comments_and_positive_comment(self):
        """
        сount_comments() returns 2 if question has 2 negative comments and doesnt get triggered
        by positive one
        """
        question_with_comments = create_question(question_text="", days=1)
        question_with_comments.comment_set.create(comment_text='', positive=False)
        question_with_comments.comment_set.create(comment_text='', positive=False)
        question_with_comments.comment_set.create(comment_text='', positive=True)
        positive_comment_amount = question_with_comments.count_comments_negative()
        self.assertEqual(positive_comment_amount, 2)

    def test_count_comments_negative_positive_comment(self):
        """
        сount_comments() doesnt get triggered by positive comment
        """
        question_with_comments = create_question(question_text="", days=1)
        question_with_comments.comment_set.create(comment_text='', positive=True)
        positive_comment_amount = question_with_comments.count_comments_negative()
        self.assertEqual(positive_comment_amount, 0)

    def test_count_comments_negative_multiple_positive_comments(self):
        """
        сount_comments() doesnt get triggered by multiple positive comments
        """
        question_with_comments = create_question(question_text="", days=1)
        question_with_comments.comment_set.create(comment_text='', positive=True)
        question_with_comments.comment_set.create(comment_text='', positive=True)
        positive_comment_amount = question_with_comments.count_comments_negative()
        self.assertEqual(positive_comment_amount, 0)
    
    def test_count_comments_negative_multiple_positive_comments_and_negative_comment(self):
        """
        сount_comments() returns 1 if question has a positive comment and doesnt get triggered
        by negative ones
        """
        question_with_comments = create_question(question_text="", days=1)
        question_with_comments.comment_set.create(comment_text='', positive=True)
        question_with_comments.comment_set.create(comment_text='', positive=True)
        question_with_comments.comment_set.create(comment_text='', positive=False)
        positive_comment_amount = question_with_comments.count_comments_negative()
        self.assertEqual(positive_comment_amount, 1)
    
    def test_count_comments_negative_multiple_positive_and_negative_comments(self):
        """
        сount_comments() returns 2 if question has 2 positive comments and doesnt get triggered
        by negative ones
        """
        question_with_comments = create_question(question_text="Question with responce", days=1)
        question_with_comments.comment_set.create(comment_text='', positive=True)
        question_with_comments.comment_set.create(comment_text='', positive=True)
        question_with_comments.comment_set.create(comment_text='', positive=False)
        question_with_comments.comment_set.create(comment_text='', positive=False)
        positive_comment_amount = question_with_comments.count_comments_negative()
        self.assertEqual(positive_comment_amount, 2)


        #TODO test negative comments: no comments, positive and negative, one of a kind, two of a kind

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
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_two_past_question(self):
        """
        Question index page may display more than one question
        """
        create_question(question_text="Past question 1", days=-30)
        create_question(question_text="Past question 2", days=-15)
        response = self.client.get(reverse('polls:index'))
        wanted_result = ['<Question: Past question 2>', '<Question: Past question 1>']
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
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

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

class QuestionChoiceViewTests(TestCase):
    def test_result_page_displays_questions_with_choices(self):
        """
        Result page is shown for pages with any choice options
        """
        question_with_choices = create_question(question_text="Question with responce", days=1)
        question_with_choices.choice_set.create(choice_text='Voted choice', votes=1)
        response = self.client.get(reverse("polls:results", args=(question_with_choices.id,)))
        self.assertEqual(response.status_code, 200)

    def test_result_page_doesnt_display_questions_without_choices(self):
        """
        Result page isn't shown for pages without any choice options
        """
        question_with_choices = create_question(question_text="Question without responce", days=1)
        response = self.client.get(reverse("polls:results", args=(question_with_choices.id,)))
        self.assertEqual(response.status_code, 404)

class QuestionCommentsViewTests(TestCase):
    def test_result_page_displays_questions_with_comments(self):
        """
        Result page is shown for pages with any comments
        """
        question_with_comments = create_question(question_text="Question with responce", days=1)
        question_with_comments.choice_set.create(choice_text='Voted choice', votes=1)
        response = self.client.get(reverse("polls:results", args=(question_with_comments.id,)))
        self.assertEqual(response.status_code, 200)

    def test_result_page_doesnt_display_questions_without_comments(self):
        """
        Result page isn't shown for pages without any comments
        """
        question_with_comments = create_question(question_text="Question without responce", days=1)
        response = self.client.get(reverse("polls:results", args=(question_with_comments.id,)))
        self.assertEqual(response.status_code, 404)