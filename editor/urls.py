from django.shortcuts import redirect
from django.urls import path

from editor.views import creation_test, editor_page

urlpatterns = [
    path('', editor_page),
    path('create_test', creation_test)
]
