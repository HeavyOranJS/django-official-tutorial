"""polls models"""
import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    """Contains question text and publishing date"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return "'{}' {}".format(
            self.question_text,
            self.pub_date.strftime("%B %d %Y"))

    def was_published_recently(self):
        """Determins if question was published less than day ago"""
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

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
