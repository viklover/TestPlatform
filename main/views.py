from django.shortcuts import render


def index_page(request):

    if not request.session.has_key('session_id'):
        return render(request, 'index.html')

    # CHANGE TO CONTINUE TEST PAGE
    return render(request, 'index.html')
