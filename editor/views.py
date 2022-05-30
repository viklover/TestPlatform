from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from editor.forms import CreationProjectForm, CreationTaskForm, EditTaskInfo, EditProjectInfo, CreationExerciseForm
from tests.models import Project, ProjectTask


@login_required
def editor_page(request):
    template = loader.get_template('editor/tests_table.html')

    columns = ['ID', 'Название', 'Заданий', 'Дата создания', 'Изменено']
    published_tests_data = []
    development_tests_data = []

    projects = Project.objects.filter(author_id=request.user.id)

    for project in projects:
        if project.published:
            published_tests_data.append(project.get_json())
        else:
            development_tests_data.append(project.get_json())

    tests_context = {
        'columns': columns,
        'type': 'tests-list',
        'class': 'development_tests'
    }

    context = {
        'published_tests_table': template.render({**tests_context, 'rows': published_tests_data}),
        'development_tests_table': template.render({**tests_context, 'rows': development_tests_data}),
        'published_tests_exists': len(published_tests_data) != 0,
        'development_tests_exists': len(development_tests_data) != 0
    }

    return render(request, template_name='editor/editor.html', context=context)


@login_required
def create_project(request):
    if not request.POST:
        return render(request, template_name='editor/creation_project.html')

    project = Project(author=request.user)
    form = CreationProjectForm(request.POST, request.FILES, instance=project)

    project = Project.create(form)

    if not project is None:
        return redirect(reverse('editor:open_project', kwargs={'project': project}))


@login_required
def open_project(request, project_id):
    template = loader.get_template('editor/tasks_table.html')

    context_table = {
        'type': 'tasks-list',
        'class': 'tasks-list',
        'columns': ['№', 'Название', 'Упражнений', 'Баллы'],
        'rows': []
    }

    for task in ProjectTask.objects.filter(project_id=project_id):
        context_table['rows'].append(task.get_json())

    context = {
        'project': Project.objects.get(id=project_id),
        'tasks_table': template.render(context_table)
    }
    return render(request, 'editor/project/project_page.html', context)


@login_required
def create_task(request, project_id):
    if request.POST:

        project = Project.objects.get(id=project_id)
        task = ProjectTask(project=project)

        form = CreationTaskForm(request.POST, instance=task)

        if project.create_task(form):
            return redirect(reverse('editor:open_task', kwargs={'project_id': project_id, 'task_id': task.id}))

    return redirect(reverse('editor:open_project', kwargs={'project_id': project_id}))


@login_required
def edit_project(request, project_id):
    if not request.POST:
        context = {
            'project': Project.objects.get(id=project_id)
        }
        return render(request, 'editor/project/project_edit.html', context)

    project = Project.objects.get(id=project_id)
    form = EditProjectInfo(request.POST, request.FILES, instance=project)

    project.edit_info(form)

    return redirect(reverse('editor:open_project', kwargs={'project_id': project_id}))


@login_required
def editor_not_allowed(request):
    return render(request, 'editor/editor_not_allowed.html') \


@login_required
def templates(request):
    return render(request, 'develop_page.html')


@login_required
def stats(request):
    return render(request, 'develop_page.html')


@login_required
def editor_modal_window(request):
    return render(request, 'modal_window.html')


@login_required
def edit_task(request, project_id, task_id):
    if not request.POST:
        context = {
            'project': Project.objects.get(id=project_id),
            'task': ProjectTask.objects.get(id=task_id)
        }
        return render(request, 'editor/project/task/task_edit.html', context)

    task = ProjectTask.objects.get(id=task_id)
    form = EditTaskInfo(request.POST, request.FILES, instance=task)

    task.edit_info(form)

    return redirect(reverse('editor:open_task', kwargs={'project_id': project_id, 'task_id': task_id}))


@login_required
def open_task(request, project_id, task_id):
    context = {
        'project': Project.objects.get(id=project_id),
        'task': ProjectTask.objects.get(id=task_id),
        'creation_exercise_form': CreationExerciseForm()
    }
    return render(request, 'editor/project/task/task_page.html', context)


@login_required
def create_exercise(request, project_id, task_id):
    if request.POST:
        form = CreationExerciseForm(request.POST)

        task = ProjectTask.objects.get(id=task_id)
        task.create_exercise(form)

    return redirect(reverse('editor:open_task', kwargs={'project_id': project_id, 'task_id': task_id}))
