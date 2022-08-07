from django.views.generic import TemplateView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User

from .models import Event, Signup
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


class EventView(DetailView):
    model = Event
    template_name = 'event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_signed_up = Signup.objects.filter(event=self.object, on_wait=False).count()
        context['num_signed_up'] = num_signed_up
        if self.request.user.is_authenticated:
            context['is_signed_up'] = Signup.objects.filter(event=self.object, user=self.request.user, on_wait=False).exists()
            context['is_on_wait'] = Signup.objects.filter(event=self.object, user=self.request.user, on_wait=True).exists()
        else:
            context['is_signed_up'] = False
            context['is_on_wait'] = False
        context['can_sign_up'] = not (context['is_signed_up'] or context['is_on_wait'])

        context['signed_up'] = User.objects.filter(signup__in=Signup.objects.filter(event=self.object, on_wait=False))
        context['waiting'] = User.objects.filter(signup__in=Signup.objects.filter(event=self.object, on_wait=True))

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


def signup(request, **kwargs):
    if request.user.is_authenticated:
        try:
            event = Event.objects.get(slug=kwargs["slug"])
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        if Signup.objects.filter(event=event, user=request.user).exists():
            return redirect("/midgardcon/program/" + kwargs["slug"])

        num_signed_up = Signup.objects.filter(event=event, on_wait=False).count()

        if num_signed_up < event.max_players:
            Signup.objects.create(event=event, user=request.user, on_wait=False)
        else:
            Signup.objects.create(event=event, user=request.user, on_wait=True)

    return redirect("/midgardcon/program/" + kwargs["slug"])


def signoff(request, **kwargs):
    if request.user.is_authenticated:
        try:
            event = Event.objects.get(slug=kwargs["slug"])
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        Signup.objects.filter(event=event, user=request.user).delete()

        num_signed_up = Signup.objects.filter(event=event, on_wait=False).count()

        while num_signed_up < event.max_players:
            if Signup.objects.filter(event=event, on_wait=True).exists():
                lucky = Signup.objects.filter(event=event, on_wait=True).order_by("time")[0]
                lucky.on_wait = False
                lucky.save()
            else:
                break
            num_signed_up = Signup.objects.filter(event=event, on_wait=False).count()

    return redirect("/midgardcon/program/" + kwargs["slug"])
