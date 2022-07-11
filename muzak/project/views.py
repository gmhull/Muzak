from django.shortcuts import render

# Create your views here.
def cover_page(request):
    return render(request, 'project/cover_page.html')

def profile(request):
    return render(request, 'project/profile.html')
