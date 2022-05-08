from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from tests.models import Test


@login_required
def editor_page(request):
    context = {
        'published_tests': Test.objects.filter(author_id=request.user.id, published=True),
        'development_tests': Test.objects.filter(author_id=request.user.id, published=False)
    }
    return render(request, template_name='editor.html', context=context)


@login_required
def creation_test(request):
    if not request.POST:
        return render(request, template_name='creation_page.html', context=context)

    return HttpResponse()