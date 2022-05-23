from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib import messages

from TestPlatform.forms import RegistrationForm
from tests.models import Test, User, Task
from tests.models.test import TestFact


def index(request):
    if not request.user.is_authenticated:
        context = {
            'tests': Test.objects.filter(published=True).order_by('-count_of_passes')[:3]
        }
        for test in context['tests']:
            print(test.name, test.description)
        return render(request, 'index.html', context)

    return your_page(request)


def register_request(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegistrationForm()
    return render(request=request, template_name="registration/registration.html", context={"form": form})


@login_required
def users_page(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, "users/users_page.html", context)


@login_required
def user_page(request, user_id):
    context = {
        'user_page': User.objects.get(id=user_id),
        'created_tests': Test.objects.filter(author=user_id),
        'finished_tests': []
    }

    for test in Test.objects.all():
        context['finished_tests'].append(test.get_statistics_differences(request.user, context['user_page']))

    return render(request=request, template_name="users/user.html", context=context)


@login_required
def your_page(request):
    return user_page(request, request.user.id)


@login_required
def edit_user_page(request):
    return render(request, 'users/user_edit.html')


@login_required
def ratings_page(request):
    context = {
        'data': []
    }

    order = 1
    for user in User.objects.order_by('-last_login')[:5]:

        stats = {
            'completed_tasks': 10,
            'amount_tasks': 37
        }
        stats['completed_in_percents'] = stats['completed_tasks'] / stats['amount_tasks']

        context['data'].append([order, user, stats])

        order += 1

    return render(request, "ratings/ratings_page.html", context)


def logout(request):
    return HttpResponse(request)
