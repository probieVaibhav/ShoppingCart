from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
# home page function
def index(request):
    return render(request, 'index.html')