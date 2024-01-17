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

def faq(request):
    return render(request, 'portal/faq.html')

def blogHome(request):
    return render(request, 'portal/blog-home.html')

def blogPost(request):
    return render(request, 'portal/blog-post.html')

def portfolioItem(request):
    return render(request, 'portal/portfolio-item.html')

def portfolioOverview(request):
    return render(request, 'portal/portfolio-overview.html')
# /home/developer/Desktop/Temp-Project/Sharma-Academy/portal/templates/portal/index.html