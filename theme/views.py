from django.views.generic import TemplateView
from .models import Event


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
