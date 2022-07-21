from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def cover_page(request):
    return render(request, 'project/cover_page.html')

@login_required
def profile(request):
    return render(request, 'project/profile.html')
