"""TestPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import settings
from .views import index, register_request, user_page, your_page, users_page, ratings_page, edit_user_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', users_page),
    path('users/<int:user_id>/', user_page),
    path('users/you/', your_page),
    path('users/you/edit/', edit_user_page),
    path('ratings/', ratings_page),
    path('tests/', include('tests.urls')),
    path('editor/', include('editor.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/', register_request, name='register'),
    path('', index)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
