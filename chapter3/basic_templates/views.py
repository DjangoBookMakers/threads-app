from django.shortcuts import render
from datetime import datetime

def index(request):
    context = {
        'page_title': 'Thread SNS',
        'welcome_message': 'Thread SNS에 오신 것을 환영합니다!',
        'current_time': datetime.now(),
        'user_count': 150
    }
    return render(request, 'basic_templates/index.html', context)

def thread_list(request):
    threads = [
        {
            'title': '첫 번째 스레드',
            'content': 'Django 템플릿 시스템을 학습하고 있습니다.',
            'author': '홍길동',
            'created_at': datetime.now(),
            'likes': 10
        },
        {
            'title': '두 번째 스레드',
            'content': '템플릿 변수와 필터를 활용해보겠습니다.',
            'author': '김철수',
            'created_at': datetime.now(),
            'likes': 15
        }
    ]
    return render(request, 'basic_templates/thread_list.html', {'threads': threads})