from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def create_ad(request):
    if request.method == 'POST':
        print(request.POST)
        print(type(request.POST))
    else:
        return render(request, 'main/create_ad.html')