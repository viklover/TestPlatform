from django.shortcuts import redirect
from django.urls import path

from editor.views import editor_page, editor_not_allowed, editor_modal_window, create_project, open_project, \
    edit_project, open_task, edit_task, create_task, create_exercise, templates, stats, remove_project, remove_task, \
    remove_element, change_element, upload_project_description, upload_task_description, create_element, publish_project

app_name = 'editor'

urlpatterns = [
    path('', editor_page, name='index'),
    path('projects/', editor_page),
    path('projects/<int:project_id>/', open_project, name='open_project'),
    path('projects/<int:project_id>/create_task', create_task, name='create_task'),
    path('projects/<int:project_id>/remove_project', remove_project, name='remove_project'),
    path('projects/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('projects/<int:project_id>/publish/', publish_project, name='publish_project'),
    path('projects/<int:project_id>/upload_description/', upload_project_description, name='upload_project_description'),
    path('projects/<int:project_id>/tasks/<int:task_id>/', open_task, name='open_task'),
    path('projects/<int:project_id>/tasks/<int:task_id>/remove_task', remove_task, name='remove_task'),
    path('projects/<int:project_id>/tasks/<int:task_id>/remove_element', remove_element, name='remove_element'),
    path('projects/<int:project_id>/tasks/<int:task_id>/change_element', change_element, name='change_element'),
    path('projects/<int:project_id>/tasks/<int:task_id>/create_exercise', create_exercise, name='create_exercise'),
    path('projects/<int:project_id>/tasks/<int:task_id>/create_element', create_element, name='create_element'),
    path('projects/<int:project_id>/tasks/<int:task_id>/upload_description/', upload_task_description, name='upload_task_description'),
    path('projects/<int:project_id>/tasks/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('create_project', create_project, name='create_project'),
    path('not_allowed', editor_not_allowed),
    path('templates', templates),
    path('stats', stats),
    path('modal_window', editor_modal_window)
]
