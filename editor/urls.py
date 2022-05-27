from django.shortcuts import redirect
from django.urls import path

from editor.views import editor_page, editor_not_allowed, editor_modal_window, create_project, open_project, \
    edit_project, open_project_task, edit_task, create_task

app_name = 'editor'

urlpatterns = [
    path('', editor_page, name='index'),
    path('projects/', editor_page),
    path('projects/<int:project_id>/', open_project, name='open_project'),
    path('projects/<int:project_id>/create_task', create_task, name='create_task'),
    path('projects/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('projects/<int:project_id>/tasks/<int:task_id>/', open_project_task, name='open_task'),
    path('projects/<int:project_id>/tasks/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('create_project', create_project, name='create_project'),
    path('not_allowed', editor_not_allowed),
    path('modal_window', editor_modal_window)
]
