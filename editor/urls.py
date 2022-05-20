from django.shortcuts import redirect
from django.urls import path

from editor.views import creation_test, editor_page, editor_not_allowed, creation_projects

urlpatterns = [
    path('', editor_page),
    path('create_test', creation_test),
    path('not_allowed', editor_not_allowed),
    path('creation_project', creation_projects)
]
