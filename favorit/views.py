from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def favorit(request):
    return render(request, 'favorit/favorit.html')