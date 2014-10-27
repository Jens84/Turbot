from django.shortcuts import render

from basic_forms.models import Question


def index(request):
    last_question = Question.objects.latest('id')
    print last_question
    context = {'last_question': last_question}
    return render(request, 'basic_forms/index.html', context)
