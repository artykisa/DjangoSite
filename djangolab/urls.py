"""djangolab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from firstapp import views
from django.views.generic import TemplateView
from firstapp.views import MemberList, GuideList
from firstapp import forms


urlpatterns = [
    path('', TemplateView.as_view(template_name="firstapp/main.html")),
    path('fivexfive/', TemplateView.as_view(template_name="firstapp/fivexfive.html")),
    path('contact/', TemplateView.as_view(template_name="firstapp/contact.html")),
    path('admin/', admin.site.urls),
    path('products/<int:productid>/', views.products),
    path('logins/', views.index),
    path('guides/cur_guide/', views.guide),
    path('addguide/', forms.GuideAddForm.as_view(), name='guide_new'),
    path('guides/<pk>/updateguide/', forms.GuideUpdateForm.as_view(), name='guide_update'),
    path('guides/<pk>/deleteguide/', forms.GuideDeleteForm.as_view(), name='delete'),
    path('guides/', GuideList.as_view()),
    path('heroes/', MemberList.as_view()),
    path('articles/', TemplateView.as_view(template_name="firstapp/articles.html")),
]
