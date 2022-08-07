import pdb

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from .models import Event
from .forms import NewUserForm


class ProgramView(TemplateView):
    template_name = "midgardconprog.html"

    def get_context_data(self, **kwargs):
        context = super(ProgramView, self).get_context_data(**kwargs)

        context['friday_rp'] = Event.objects.filter(start_time__week_day=6, category='RP').order_by('start_time')
        context['friday_bg'] = Event.objects.filter(start_time__week_day=6, category='BG').order_by('start_time')
        context['friday_na'] = Event.objects.filter(start_time__week_day=6, category='NA').order_by('start_time')

        context['saturday_rp'] = Event.objects.filter(start_time__week_day=7, category='RP').order_by('start_time')
        context['saturday_bg'] = Event.objects.filter(start_time__week_day=7, category='BG').order_by('start_time')
        context['saturday_na'] = Event.objects.filter(start_time__week_day=7, category='NA').order_by('start_time')

        context['sunday_rp'] = Event.objects.filter(start_time__week_day=1, category='RP').order_by('start_time')
        context['sunday_bg'] = Event.objects.filter(start_time__week_day=1, category='BG').order_by('start_time')
        context['sunday_na'] = Event.objects.filter(start_time__week_day=1, category='NA').order_by('start_time')

        return context


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registrering fullført.")
            return redirect("midgardcon")
        messages.error(request, "Registrering feilet. Sjekk felt.")
        for e in form.errors:
            for msg in form.errors[e]:
                messages.error(request, msg)
    form = NewUserForm()
    return render(request=request, template_name="registrer.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Du er logget inn som {username}.")
                return redirect("midgardcon")
            else:
                messages.error(request, "Feil brukernavn eller passord.")
        else:
            messages.error(request, "Feil brukernavn eller passord.")
    form = AuthenticationForm()
    return render(request=request, template_name="logginn.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Du har logget ut.")
    return redirect("midgardcon")
