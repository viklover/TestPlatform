from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tests.models import Test, Task


def tests_page(request):
    context = {
        'tests': Test.objects.filter(published=True)
    }
    return render(request, 'tests_page.html', context)


def test_page(request, test_id):
    context = {
        'test': Test.objects.get(id=test_id)
    }
    return render(request, 'test_page.html', context)


@login_required
def open_test(request, test_id):
    tasks = Task.objects.filter(test=test_id).order_by('number')
    context = {
        'test': Test.objects.get(id=test_id),
        'task': tasks.first(),
        'tasks': tasks
    }
    return render(request, 'task.html', context)


@login_required
def open_task(request, test_id, task_number):
    tasks = Task.objects.filter(test=test_id).order_by('number')
    context = {
        'test': Test.objects.get(id=test_id),
        'task': tasks.get(task_number),
        'tasks': tasks
    }
    return render(request, 'task.html', context)
