from django.shortcuts import redirect
from django.urls import path

from editor.views import editor_page, editor_not_allowed, editor_modal_window, create_project, open_project, \
    edit_project, open_project_task, edit_task, create_task

urlpatterns = [
    path('', editor_page),
    path('tests/', editor_page),
    path('tests/<int:test_id>/', open_project),
    path('tests/<int:test_id>/create_task', create_task),
    path('tests/<int:test_id>/edit/', edit_project),
    path('tests/<int:test_id>/tasks/<int:task_id>/', open_project_task),
    path('tests/<int:test_id>/tasks/<int:task_id>/edit/', edit_task),
    path('create_project', create_project),
    path('not_allowed', editor_not_allowed),
    path('modal_window', editor_modal_window)
]
