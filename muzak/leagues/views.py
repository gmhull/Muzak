from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def league_home(request):
    return render(request, 'leagues/league_home.html')
