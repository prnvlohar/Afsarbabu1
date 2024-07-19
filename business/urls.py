
from django.urls import path

from business.views import (home, about, contact, pricing, blogHome, blogPost1, blogPost2, blogPost3)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('pricing/', pricing, name='pricing'),
    path('blog-home/', blogHome, name='blog-home'),
    path('blog-post1/', blogPost1, name='blog-post1'),
    path('blog-post2/', blogPost2, name='blog-post2'),
    path('blog-post3/', blogPost3, name='blog-post3')
]
