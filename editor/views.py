from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from editor.forms import CreationTestForm
from tests.models import Test


@login_required
def editor_page(request):
    context = {
        'published_tests': Test.objects.filter(author_id=request.user.id, published=True),
        'development_tests': Test.objects.filter(author_id=request.user.id, published=False)
    }
    return render(request, template_name='editor/editor.html', context=context)


@login_required
def creation_test(request):

    if not request.POST:
        context = {
            'form': CreationTestForm(
                initial={
                  'author': request.user
                }
            )
        }
        return render(request, template_name='editor/creation_page.html', context=context)

    test = Test(author=request.user)
    form = CreationTestForm(request.POST, request.FILES, instance=test)

    if form.is_valid():
        test = form.save(commit=False)
        test.save()
        return redirect(f'/editor/tests/{test.id}')

