from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Organizer(models.Model):
    name = models.CharField(max_length=50, verbose_name="navn på arrangør")
    email = models.EmailField(blank=True)

    class Meta:
        verbose_name = "kontaktperson"
        verbose_name_plural = "kontaktpersoner"

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50, verbose_name="navn på arrangement")
    CATEGORIES = (
        ('RP', "Rollespill"),
        ('BG', "Brettspill"),
        ('NA', "Annet")
    )
    category = models.CharField(max_length=2, choices=CATEGORIES)
    start_time = models.DateTimeField(verbose_name="starttidspunkt")
    end_time = models.DateTimeField(verbose_name="slutttidspunkt")
    max_players = models.IntegerField(verbose_name="maks antall spillere", default=0)
    contact = models.ForeignKey(to=Organizer, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name="kontaktperson")
    location = models.CharField(max_length=30, verbose_name="plassering", blank=True)
    description = models.TextField(blank=True)

    slug = models.SlugField(blank=True)

    @property
    def num_signed_up(self):
        return Signup.objects.filter(event=self).count()

    class Meta:
        verbose_name = "arrangement"
        verbose_name_plural = "arrangementer"
        ordering = ["start_time"]

    def __str__(self):
        return self.name + ", " + self.start_time.strftime("%a %H:%M")

    def save(self, *args, **kwargs):
        self.slug = slugify(self)
        super(Event, self).save(*args, **kwargs)


class Signup(models.Model):
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    on_wait = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "påmelding"
        verbose_name_plural = "påmeldinger"
        ordering = ["event", "time"]

    def __str__(self):
        name = str(self.event) + ", " + str(self.user)
        if self.on_wait:
            name += ", venteliste"
        return name
