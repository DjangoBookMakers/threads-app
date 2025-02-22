from django.shortcuts import render
from datetime import datetime

def index(request):
    context = {
        'page_title': 'Thread SNS',
        'welcome_message': 'Thread SNS에 오신 것을 환영합니다!',
        'current_time': datetime.now(),
        'user_count': 150,
        'trending_tags': ['Django', 'Python', 'Web개발', '프로그래밍']
    }
    return render(request, 'basic_templates/index.html', context)

def thread_list(request):
    context = {
        'threads': [
            {
                'title': '첫 번째 스레드',
                'content': 'Django 템플릿 시스템을 학습하고 있습니다.',
                'author': '홍길동',
                'created_at': datetime.now(),
                'likes': 10
            },
            {
                'title': '두 번째 스레드',
                'content': '템플릿 상속과 재사용을 배우고 있습니다.',
                'author': '김철수',
                'created_at': datetime.now(),
                'likes': 15
            }
        ],
        'trending_tags': ['Django', 'Python', 'Web개발', '프로그래밍']
    }
    return render(request, 'basic_templates/thread_list.html', context)