from django.shortcuts import render


# TODO: move to users views ???
def login(request):
    return render(request, 'login.html')


# TODO: move to users views ???
def client(request):
    return render(request, 'client.html')


def clients(request):
    return render(request, 'clients.html')


def orders(request):
    return render(request, 'orders.html')


def report(request):
    return render(request, 'report.html')


def salary(request):
    return render(request, 'salary.html')
