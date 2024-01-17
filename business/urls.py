
from django.urls import path

from business.views import (home, about, contact, pricing, faq, blogHome, blogPost, portfolioItem, portfolioOverview)

urlpatterns = [
    path('h', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('pricing/', pricing, name='pricing'),
    path('faq/', faq, name='faq'),
    path('blog-home/', blogHome, name='blog-home'),
    path('blog-post/', blogPost, name='blog-post'),
    path('portfolio-item/', portfolioItem, name='portfolio-item'),
    path('portfolio-overview/', portfolioOverview, name='portfolio-overview'),

]
