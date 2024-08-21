from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.core.exceptions import ValidationError

import os


# Create your forms here.
def validate_code(value):
    if value != os.environ.get('REGISTER_CODE'):
        raise ValidationError(
            _('%(value)s er ikke rett kode.'),
            params={'value': value},
        )


def check_checkbox(value):
    if not value:
        raise ValidationError(
            _('Du har ikke godtatt at dine personopplysninger behandles'),
        )


class NewUserForm(UserCreationForm):
    username = forms.RegexField(label=_("Email"), max_length=150,
                                regex=r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w+)+$',
                                help_text=_("Fungerer som brukernavn. Bokstaver, tall og @/./+/-/_ tegn."),
                                error_messages={'invalid': _(
                                    "Må være en gyldig epostadresse, med bokstaver, tall og @/./+/-/_ tegn.")})

    password1 = forms.CharField(
        label=_("Passord"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Bekreft passord"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Skriv samme passord som over."),
    )

    register_code = forms.CharField(
        label=_("Kode fra billettkjøp"),
        help_text=_("Sjekk epost fra TicketCo. NB: ikke \"referansekode\"."),
        required=True,
    )

    checkbox_terms = forms.BooleanField(
        label=_(""),
        help_text=_("Jeg godtar at mine personopplysninger ovenfor behandles i sammenheng med organisering av MidgardCon 2024."),
        required=True,
    )

    register_code.validators.append(validate_code)
    checkbox_terms.validators.append(check_checkbox)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2", "register_code", "checkbox_terms")
        labels = {
            'first_name': 'Fornavn',
            'last_name': 'Etternavn',
        }

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['username']
        if commit:
            user.save()
        return user
