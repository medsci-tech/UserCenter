# 模板
# coding:utf-8
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def button(request):
    return render(request, 'button.html')
def calendar(request):
    return render(request, 'calendar.html')
def charts(request):
    return render(request, 'charts.html')
def chat(request):
    return render(request, 'chat.html')
def gallery(request):
    return render(request, 'gallery.html')
def grid(request):
    return render(request, 'grid.html')
def interface(request):
    return render(request, 'interface.html')
def invoice(request):
    return render(request, 'invoice.html')
def login(request):
    return render(request, 'login.html')
def massage(request):
    return render(request, 'massage.html')
def tables(request):
    return render(request, 'tables.html')
def widgets(request):
    return render(request, 'widgets.html')

