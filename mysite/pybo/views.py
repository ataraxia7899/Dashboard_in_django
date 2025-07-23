from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
  return render(request, 'dashboard.html')
def post_list(request):
  return render(request, 'post_list.html')