from django.shortcuts import render


def HomePage(request):
    return render(request, 'home.html')


def RegisterUser(request):
    return render(request, 'register.html')
