from django.shortcuts import render

from basic_forms.models import Question
from basic_forms.models import QuestionForm
from basic_forms.models import Answer


def index(request):
    answer = ""
    if request.method == 'POST':
        q = QuestionForm(request.POST)
        print q
        if q.is_valid():
            q.save()

        #TODO : find an answer
        answer = Answer.objects.latest('id')

    try:
        last_question = Question.objects.latest('id')
        print last_question

    except:
        last_question = ""

    context = {'last_question': last_question}
    context = {'answer': answer}
    return render(request, 'basic_forms/index.html', context)
