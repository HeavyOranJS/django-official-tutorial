"""polls models"""
import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    """Contains question text and publishing date"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return "{}".format(
            self.question_text)

    def count_comments(self):
        """
        Returns amount of comments
        """
        return Question.objects.get(pk=self.pk).comment_set.all().count()

    def count_comments_positive(self):
        """
        Returns amount of positive comments
        """
        return Question.objects.get(pk=self.pk).comment_set.filter(positive=True).count()

    def count_comments_negative(self):
        """
        Returns amount of negative comments
        """
        return Question.objects.get(pk=self.pk).comment_set.filter(positive=False).count()

    def was_published_recently(self):
        """Determins if question was published less than day ago"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    #admin dashboard options
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    count_comments.short_description = "Comments"
    count_comments_positive.short_description = "Postive"
    count_comments_negative.short_description = "Negative"

class Comment(models.Model):
    """Comments to question. Contains link to question, comment text and bool positive"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    positive = models.BooleanField(default=True)

    def __str__(self):
        return "{}. {}: '{}'".format(
            "Positive" if self.positive else "Negative",
            self.question,
            self.comment_text)

    #admin dashboard options
    positive.boolean = True
    positive.short_description = 'Comment raiting'

class Choice(models.Model):
    """Vote options to question. Contains link to question, option text and amount of votes"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return "{0}, choice: '{1}', votes: {2}".format(
            self.question,
            self.choice_text,
            self.votes)
