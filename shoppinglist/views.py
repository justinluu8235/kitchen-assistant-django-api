from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic


def index(request):
    template_name = 'shoppinglist/index.html'
    return template_name