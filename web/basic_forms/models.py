from django.db import models
from django.forms import ModelForm


class Question(models.Model):
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['content']


class Answer(models.Model):
    question = models.ForeignKey(Question)
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content
