from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from tests.models import Test, Task
from tests.models.test import TestComment


def tests_page(request):
    context = {
        'tests': Test.objects.filter(published=True)
    }
    return render(request, 'tests/tests_page.html', context)


def test_page(request, test_id):
    context = {
        'test': Test.objects.get(id=test_id),
        'comments': TestComment.objects.filter(test_id=test_id).order_by('-published_at')
    }
    return render(request, 'tests/test_page.html', context)


@login_required
def open_test(request, test_id):
    return redirect(f'/tests/{test_id}/tasks/1')


@login_required
def upload_comment(request, test_id):

    if request.POST and request.POST.get('text', None) is not None:
        comment = TestComment()
        comment.test = Test.objects.get(id=test_id)
        comment.user = request.user
        comment.message = request.POST['text']
        comment.save()
        return redirect(f'/tests/{test_id}')

    return open_test(request, test_id)


@login_required
def open_task(request, test_id, task_number):
    tasks = Task.objects.filter(test=test_id).order_by('number')

    try:
        current_task = tasks.get(number=task_number)
    except Exception:
        return redirect(f'/tests/{test_id}/tasks')

    context = {
        'test': Test.objects.get(id=test_id),
        'task': current_task,
        'tasks': tasks
    }
    return render(request, 'tests/test/task_page.html', context)
