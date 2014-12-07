from django.shortcuts import render

from basic_forms.models import Question
from basic_forms.models import QuestionForm

from turbot import Turbot


class MainView():
    _turbot = None

    def __init__(self):
        if not self._turbot:
            self._turbot = Turbot()

    def index(self, request):
        answer = ""
        if request.method == 'POST':
            q = QuestionForm(request.POST)
            if q.is_valid():
                q.save()

            last = Question.objects.latest('id')
            answer = self._turbot.answer(last.content)

        try:
            last_question = Question.objects.latest('id')

        except:
            last_question.content = ""

        context = {'last_question': last_question.content, 'answer': answer}
        return render(request, 'basic_forms/index.html', context)
