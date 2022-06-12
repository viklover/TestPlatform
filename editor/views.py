import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from editor.forms import CreationProjectForm, CreationTaskForm, EditTaskInfo, EditProjectInfo, CreationExerciseForm, \
    CheckMarkDownForm, CreationStaticElementForm

from tests.models import Project, ProjectTask, ProjectTaskElement, BaseExercise, \
    ChronologyExercise, MatchExercise, InputExercise, AnswerExercise, RadioExercise, StatementsExercise, \
    ImagesExercise, BaseElement, BaseStaticElement


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
        return redirect(reverse('editor:open_project', kwargs={'project_id': project.id}))


@login_required
def remove_project(request, project_id):
    if request.POST:
        project = Project.objects.get(id=project_id)
        if project.project_name == request.POST.get('input_projectname', None):
            project.delete()
            return redirect(reverse('editor:index'))

    return redirect(reverse('editor:open_project', kwargs={'project_id': project_id}))


@login_required
def open_project(request, project_id):
    if request.POST:
        data = json.loads(request.POST['json'])
        if 'tasks_table' in data:
            project = Project.objects.get(id=project_id)
            if len(data['tasks_table']) == project.number_of_tasks:
                for number, task_id in enumerate(data['tasks_table']):
                    task = ProjectTask.objects.get(id=task_id)
                    task.number = number + 1
                    task.save()

    template = loader.get_template('editor/tasks_table.html')

    context_table = {
        'type': 'tasks-list',
        'class': 'tasks-list',
        'columns': ['№', 'Название', 'Упражнений', 'Баллы'],
        'rows': []
    }

    is_empty = True

    for task in ProjectTask.objects.filter(project_id=project_id).order_by('number'):
        context_table['rows'].append(task.get_json())
        is_empty = False

    context = {
        'project': Project.objects.get(id=project_id),
        'tasks_table': template.render(context_table),
        'is_empty': is_empty
    }
    return render(request, 'editor/project/project_page.html', context)


@login_required
def create_task(request, project_id):
    if request.POST:

        project = Project.objects.get(id=project_id)
        task = ProjectTask(project=project)

        form = CreationTaskForm(request.POST, instance=task)

        if project.create_task(form):
            project.number_of_tasks += 1
            project.save()
            return redirect(reverse('editor:open_task', kwargs={'project_id': project_id, 'task_id': task.id}))

    return redirect(reverse('editor:open_project', kwargs={'project_id': project_id}))


@login_required
def remove_task(request, project_id, task_id):
    if request.POST:
        selected_task = ProjectTask.objects.get(id=task_id)
        number = selected_task.number
        for task in ProjectTask.objects.filter(project_id=project_id, number__gt=number).order_by('number'):
            task.number = number
            task.save()
            number += 1
        selected_task.delete()
        return redirect(reverse('editor:open_project', kwargs={'project_id': project_id}))

    return redirect(reverse('editor:open_task', kwargs={'project_id': project_id, 'task_id': task_id}))


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
    return render(request, 'editor/editor_not_allowed.html')


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
    if request.POST:
        data = json.loads(request.POST['json'])
        if 'elements-ordering' in data:
            number_of_elements = ProjectTaskElement.objects.filter(task_id=task_id).count()
            print(number_of_elements)
            if len(data['elements-ordering']) == number_of_elements:
                for index, elem_id in enumerate(data['elements-ordering']):
                    element = ProjectTaskElement.objects.get(element_id=elem_id)
                    element.order = index + 1
                    element.save()

    context = {
        'project': Project.objects.get(id=project_id),
        'task': ProjectTask.objects.get(id=task_id),
        'elements': map(lambda x: x.get_child(), ProjectTaskElement.objects.filter(task_id=task_id).order_by('order')),
        'creation_exercise_form': CreationExerciseForm(),
        'creation_element_form': CreationStaticElementForm()
    }
    return render(request, 'editor/project/task/task_page.html', context)


@login_required
def upload_project_description(request, project_id):

    form = CheckMarkDownForm(request.POST)

    if form.is_valid():
        project = Project.objects.get(id=project_id)
        project.description_md = request.POST.get('markdown_field')
        project.save()

    # return redirect(reverse('editor:open_project', kwargs={'project_id': project_id}))
    return JsonResponse({})


@login_required
def upload_task_description(request, project_id, task_id):

    form = CheckMarkDownForm(request.POST)

    if form.is_valid():
        task = ProjectTask.objects.get(id=task_id)
        task.description_md = request.POST.get('markdown_field')
        task.save()

    return JsonResponse({})


@login_required
def create_element(request, project_id, task_id):
    if request.POST:
        form = CreationStaticElementForm(request.POST)

        task = ProjectTask.objects.get(id=task_id)
        task.create_element(form)

    return redirect(reverse('editor:open_task', kwargs={'project_id': project_id, 'task_id': task_id}))


@login_required
def create_exercise(request, project_id, task_id):
    if request.POST:
        form = CreationExerciseForm(request.POST)

        task = ProjectTask.objects.get(id=task_id)
        task.create_exercise(form)

    return redirect(reverse('editor:open_task', kwargs={'project_id': project_id, 'task_id': task_id}))


@login_required
def remove_element(request, project_id, task_id):
    if request.POST and request.POST.get('element_id', False):
        elem_id = request.POST.get('element_id')
        selected_element = ProjectTaskElement.objects.get(element_id=elem_id)
        order = selected_element.order
        for element in ProjectTaskElement.objects.filter(task_id=task_id, order__gt=order).order_by('order'):
            element.order = order
            element.save()
            order += 1
        selected_element.delete()
        return redirect(reverse('editor:open_task', kwargs={'project_id': project_id, 'task_id': task_id}))

    return redirect(reverse('editor:open_task', kwargs={'project_id': project_id, 'task_id': task_id}))


@login_required
def change_element(request, project_id, task_id):
    print(request.POST)

    if request.POST and request.POST.get('element_id', False):
        elem_id = request.POST.get('element_id')
        selected_element = ProjectTaskElement.objects.get(element_id=elem_id).get_child()

        if selected_element.element_type == 0:

            if request.POST.get('title', False) or request.POST.get('title', False) == "":
                selected_element.title = request.POST.get('title')
                selected_element.save()

            if request.POST.get('only_title', False):
                return HttpResponse()

            return JsonResponse(eval(f'{BaseExercise.EXERCISE_CLASSES[selected_element.exercise_type]}.process_request(request, selected_element)'))

        elif selected_element.element_type == 1:
            return JsonResponse(eval(f'{BaseStaticElement.ELEMENT_CLASSES[selected_element.static_element_type]}.process_request(request, selected_element)'))

        return redirect(reverse('editor:open_project', kwargs={'project_id': project_id}))

    return redirect(reverse('editor:open_task', kwargs={'project_id': project_id, 'task_id': task_id}))


