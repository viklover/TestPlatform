from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from editor.forms import CreationTestForm
from tests.models import Test, Task


@login_required
def editor_page(request):
    template = loader.get_template('table.html')

    columns = ['ID', 'Название', 'Заданий', 'Дата создания', 'Изменено']
    published_tests_rows = []
    development_tests_rows = []

    tests = Test.objects.filter(author_id=request.user.id)
    published_tests = tests.filter(published=True)
    development_tests = tests.filter(published=False)

    for test in tests:
        if test.published:
            published_tests_rows.append(test.get_json())
        else:
            development_tests_rows.append(test.get_json())

    tests_context = {
        'columns': columns,
        'type': 'tests-list'
    }

    context = {
        'published_tests': published_tests,
        'development_tests': development_tests,
        'published_tests_table': template.render({**tests_context, 'rows': published_tests_rows, 'class': 'published_tests'}),
        'development_tests_table': template.render({**tests_context, 'rows': development_tests_rows, 'class': 'development_tests'})
    }

    return render(request, template_name='editor/editor.html', context=context)


@login_required
def create_project(request):
    if not request.POST:
        return render(request, template_name='editor/project/creation_project.html')

    test = Test(author=request.user)
    form = CreationTestForm(request.POST, request.FILES, instance=test)

    if form.is_valid():
        test = form.save(commit=False)
        test.save()
        return redirect(f'/editor/tests/{test.id}')


@login_required
def open_project(request, test_id):

    template = loader.get_template('table.html')

    context_table = {
        'type': 'tasks-list',
        'class': 'tasks-list',
        'columns': ['№', 'Название', 'Упражнений', 'Баллы'],
        'rows': []
    }

    for task in Task.objects.filter(test_id=test_id):
        context_table['rows'].append(task.get_json())

    context = {
        'test': Test.objects.get(id=test_id),
        'tasks_table': template.render(context_table)
    }
    return render(request, 'editor/project/project_page.html', context)


@login_required
def editor_not_allowed(request):
    return render(request, 'editor/editor_not_allowed.html')


@login_required
def editor_modal_window(request):
    return render(request, 'modal_window.html')
