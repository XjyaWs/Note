from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect


def index_view(request):
    return render(request, 'index.html')


def blank_view(request):
    return HttpResponseRedirect(reverse('index'))