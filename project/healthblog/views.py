from django.shortcuts import render

# Create your views here.
def BlogHome(request):
    return render(request,'blog/BlogHome.html')