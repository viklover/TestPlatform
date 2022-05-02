from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from tests.models import Test


def index(request):
    context = {
        'tests': Test.objects.all()
    }
    for test in context['tests']:
        print(test.name, test.description)
    return render(request, 'index.html', context)


def login(request):
    return HttpResponse(request)


def logout(request):
    return HttpResponse(request)
