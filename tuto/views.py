from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, tuto. You're at the polls index.")
