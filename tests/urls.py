from django.shortcuts import redirect
from django.urls import path

from tests.views import test_page, open_test

urlpatterns = [
    path('<int:test_id>', test_page),
    path('<int:test_id>/start', open_test),
]