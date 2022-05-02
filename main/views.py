import os
import json

from django.http import HttpResponse, JsonResponse
from django.template import loader, Context, TemplateDoesNotExist
from django.shortcuts import render, redirect

from PostReformRussia.settings import BASE_DIR


def index_page(request):
    if not request.session.has_key('session_id'):
        return render(request, 'index.html')

    # CHANGE TO CONTINUE TEST PAGE
    return render(request, 'index.html')


def start_test(request):
    return redirect('tasks/1')
    # return open_task(request, 1)


def open_task(request, task_id):
    task = f'task{task_id}'

    context = {}

    with open(os.path.join(BASE_DIR, 'main', 'templates', 'tasks', task, 'content.json'), 'r', encoding="utf-8") as f:
        data = json.load(f)

    for exercise in data['exercises']:
        try:
            template = loader.get_template(f'exercises/{exercise["type"]}.html')
            context[exercise['field_name']] = template.render({**exercise, **exercise['context']})
        except TemplateDoesNotExist:
            context[exercise['field_name']] = ''

    return render(request, f'tasks/{task}/page.html', context)


def check_answer(request, task_id):
    response = HttpResponse()

    print(dir(request.GET))
    print(request.content_params)
    print(request.body.decode("utf-8"))
    # print(json.loads(request.body))

    if request.method == 'GET':
        return JsonResponse(json.loads(request.body.decode("utf-8")))

    return response
