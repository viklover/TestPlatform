"""PostReformRussia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from PostReformRussia import settings
from main.views import index_page, start_test, open_task, check_answer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('start', start_test),
    path('tasks/<int:task_id>/send', check_answer),
    path('tasks/<int:task_id>/', open_task)
]
# static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


