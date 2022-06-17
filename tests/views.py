from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from tests.models import Test
from tests.models.test import TestComment, TestFact


@login_required
def tests_page(request):
    context = {
        'tests': [test.render() for test in Test.objects.all()]
    }
    return render(request, 'tests/tests_page.html', context)


def test_page(request, test_id):
    test = Test.objects.get(id=test_id)

    context = {
        'test': test,
        'number_of_tasks': test.project.number_of_tasks,
        'number_of_facts': TestFact.objects.filter(test=test).count(),
        'comments': TestComment.objects.filter(test_id=test_id).order_by('-published_at')
    }
    return render(request, 'tests/test_page.html', context)


@login_required
def open_test(request, test_id):
    test = Test.objects.get(id=test_id)

    if not TestFact.has_session(request.user, test_id):
        test.start(request.user)

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

    if not TestFact.has_session(request.user, test_id):
        return redirect(reverse('tests:test_page', kwargs={'test_id': test_id}))

    session = TestFact.get_session(request.user, test_id)
    tasks = session.get_tasks()

    try:
        current_task = tasks.get(number=task_number)
    except Exception:
        return redirect(reverse('tests:open_task', kwargs={'test_id': test_id, 'task_number': 1}))

    context = {
        'test': Test.objects.get(id=test_id),
        'task': current_task,
        'elements': [obj.get_child() for obj in current_task.get_elements()],
        'tasks': tasks
    }
    return render(request, 'tests/test/task_page.html', context)


@login_required
def open_tasks_page(request, test_id):

    if not TestFact.has_session(request.user, test_id):
        return redirect(reverse('tests:test_page', kwargs={'test_id': test_id}))

    context = {
        'test': Test.objects.get(id=test_id),
        'tasks': TestFact.get_session(request.user, test_id).get_tasks()
    }
    return render(request, 'tests/test/tasks_page.html', context)


@login_required
def finish_test(request, test_id):

    if TestFact.has_session(request.user, test_id):
        test_fact = TestFact.get_session(request.user, test_id)
        test_fact.finish()
        return redirect(reverse('tests:fact_page', kwargs={'fact_id': test_fact.id}))

    return redirect(reverse('tests:tests_page'))



@login_required
def result_page(request, test_id):
    context = {
        'test': Test.objects.get(id=test_id)
    }
    return render(request, 'tests/test_result.html', context)


@login_required
def fact_page(request, fact_id):
    context = {
        'fact': TestFact.objects.get(id=fact_id)
    }

    if not context['fact'].user.id == request.user.id:
        return redirect(reverse('tests:tests_page'))

    return render(request, 'tests/test_result.html', context)


@login_required
def remove_fact(request, fact_id):
    fact = TestFact.objects.get(id=fact_id)
    test_id = fact.test_id
    fact.delete()

    return redirect(reverse('tests:test_page', kwargs={'test_id': test_id}))
