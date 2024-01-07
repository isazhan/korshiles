from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def create_ad(request):
    return render(request, 'main/create_ad.html')