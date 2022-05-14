from django.shortcuts import redirect
from django.urls import path

from tests.views import test_page, open_test, tests_page, upload_comment

urlpatterns = [
    path('', tests_page),
    path('<int:test_id>', test_page),
    path('<int:test_id>/upload_comment', upload_comment),
    path('<int:test_id>/start', open_test),
]
