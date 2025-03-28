from django.shortcuts import render


def home(request):
    """
    홈 페이지 뷰 - 로그인한 사용자의 타임라인을 표시합니다.
    """
    context = {
        "title": "홈",
    }
    return render(request, "threads/home.html", context)


def explore(request):
    """
    탐색 페이지 뷰 - 인기 스레드와 트렌드를 표시합니다.
    """
    context = {
        "title": "탐색",
    }
    return render(request, "threads/explore.html", context)
