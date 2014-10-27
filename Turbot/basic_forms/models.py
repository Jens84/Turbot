from django.db import models


class Question(models.Model):
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content


class Answer(models.Model):
    question = models.ForeignKey(Question)
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content
