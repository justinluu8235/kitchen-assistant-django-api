from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic


def index(request):
    template_name = 'recipes/index.html'
    return template_name

# class IndexView(generic.ListView):
#     template_name = 'recipes/index.html'

#     # def get_queryset(self):
     
#     #     return None