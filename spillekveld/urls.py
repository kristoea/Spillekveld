"""spillekveld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.views.generic import TemplateView

from theme.views import ProgramView, register_request, login_request, logout_request, EventView, signup, signoff

urlpatterns = [
    path('', TemplateView.as_view(template_name="base.html")),
    path('midgardcon/', TemplateView.as_view(template_name="midgardcon.html"), name="midgardcon"),
    path('midgardcon/program/', ProgramView.as_view(template_name="midgardconprog.html"), name="program"),
    path('midgardcon/skrivekonkurranse/', ProgramView.as_view(template_name="skrivekonkurranse.html"), name="program"),
    path('midgardcon/midgardconishprogram/', ProgramView.as_view(template_name="midgardconishprog.html"), name="midgardconishprogram"),
    path('admin/', admin.site.urls),
    path("midgardcon/registrer/", register_request, name="registrer"),
    path("midgardcon/logginn/", login_request, name="logginn"),
    path("midgardcon/loggut/", logout_request, name="loggut"),
    path('midgardcon/program/<slug:slug>/', EventView.as_view(), name='event-detail'),
    path('midgardcon/program/<slug:slug>/signup', signup, name='event-signup'),
    path('midgardcon/program/<slug:slug>/signoff', signoff, name='event-signoff'),
]
