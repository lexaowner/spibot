from django.shortcuts import render

def start_page(requests):
    return render(requests,'tester/base.html')
