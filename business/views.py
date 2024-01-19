from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'portal/index.html')

def about(request):
    return render(request, 'portal/about.html')

def contact(request):
    return render(request, 'portal/contact.html')

def pricing(request):
    return render(request, 'portal/pricing.html')


def blogHome(request):
    return render(request, 'portal/blog-home.html')

def blogPost1(request):
    return render(request, 'portal/blog-post1.html')
def blogPost2(request):
    return render(request, 'portal/blog-post2.html')
def blogPost3(request):
    return render(request, 'portal/blog-post3.html')
