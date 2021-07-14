from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def peta(request):
    return render(request, 'peta.html')


def statistik(request):
    return render(request, 'statistik.html')
