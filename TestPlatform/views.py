from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib import messages

# Create your views here.
from TestPlatform.forms import RegistrationForm
from tests.models import Test, User


def index(request):
    context = {
        'tests': Test.objects.filter(published=True).order_by('-count_of_passes')[:3]
    }
    for test in context['tests']:
        print(test.name, test.description)
    return render(request, 'index.html', context)


def register_request(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegistrationForm()
    return render(request=request, template_name="registration/registration.html", context={"register_form": form})


@login_required
def user_page(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request=request, template_name="users/user.html", context=context)


def logout(request):
    return HttpResponse(request)
