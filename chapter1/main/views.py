from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse("<h1>메인 페이지입니다.</h1>")
    return render(request, "main/index.html")


def a(request):
    # return HttpResponse("<h1>A 페이지입니다.</h1>")
    return render(request, "main/a.html")


def b(request):
    # return HttpResponse("<h1>B 페이지입니다.</h1>")
    return render(request, "main/b.html")


def c(request):
    # return HttpResponse("<h1>C 페이지입니다.</h1>")
    return render(request, "main/c.html")


def hojun(request):
    # return HttpResponse("<h1>이호준 소개 페이지입니다.</h1>")
    return render(request, "main/hojun.html")


def orm(request):
    # return HttpResponse("<h1>ORM 소개 페이지입니다.</h1>")
    return render(request, "main/orm.html")
