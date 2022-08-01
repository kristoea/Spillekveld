from django.db import models


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

    class Meta:
        verbose_name = "arrangement"
        verbose_name_plural = "arrangementer"
        ordering = ["start_time"]

    def __str__(self):
        return self.name + ", " + self.start_time.strftime("%a %H:%M")
