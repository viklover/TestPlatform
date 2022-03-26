from django.shortcuts import render


def index_page(request):
    if not request.session.has_key('session_id'):
        return render(request, 'index.html')

    # CHANGE TO CONTINUE TEST PAGE
    return render(request, 'index.html')


def start_test(request):
    return open_task(request, 1)


def open_task(request, task):

    context = {}

    if task == 1:
        context = {
            'type1': [
                'Начало правления Николая II',
                'Манифест об отмене крепостного права',
                'Крымская война',
                'Земская реформа',
                'Строительство Транссибирской магистрали'
            ]
        }

    # if task == 5:
    #     context = {
    #         'type5': [
    #             'За счёт государственной казны',
    #             'При помощи помещиков',
    #             'За собственный выкуп при помощи государства'
    #         ]
    #     }

    return render(request, f'tasks/task{task}.html', context)
