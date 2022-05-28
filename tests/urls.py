from django.shortcuts import redirect
from django.urls import path

from tests.views import test_page, open_test, tests_page, upload_comment, open_task

app_name = 'tests'

urlpatterns = [
    path('', tests_page, name='index'),
    path('<int:test_id>', test_page, name='test_page'),
    path('<int:test_id>/upload_comment', upload_comment, name='upload_comment'),
    path('<int:test_id>/start', open_test, name='start_test'),
    path('<int:test_id>/tasks/<int:task_number>/', open_task, name='open_task'),
]
