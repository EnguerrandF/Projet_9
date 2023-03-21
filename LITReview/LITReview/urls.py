"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from blog.views import home_page, creation_ticket, modify_ticket, remove_ticket, creation_review, modify_review, remove_review
from authentication.views import signup_page, logout_page, LoginPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginPage.as_view(), name='login'),
    path('home/', home_page, name='home'),
    path('signup/', signup_page, name='signup'),
    path('logout/', logout_page, name='logout'),
    path('home/ticket/creation', creation_ticket, name='creation_ticket'),
    path('home/ticket/<int:id>/modify', modify_ticket, name='modify_ticket'),
    path('home/ticket/<int:id>/delete', remove_ticket, name='remove_ticket'),
    path('home/critique/<int:id>/creation', creation_review, name='creation_review'),
    path('home/critique/<int:id>/modify', modify_review, name='modify_review'),
    path('home/critique/<int:id>/remove', remove_review, name='remove_review'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
