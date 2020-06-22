from django.contrib import admin
from .models import Heroes, Guide, Items, Neutrals, Role, Runes, Profile
from django.template.loader import render_to_string
from django.contrib import admin
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from gevent.pool import Pool
from .tokens import account_activation_token
import datetime
from django.contrib.sites.shortcuts import get_current_site
from jinja2 import Template


# Register your models here.

def send(queryset_user):
    template = Template("""
    Date/time: {{ now() }}
    Hi {{ user.username }} ({{ user.email }}),
    Please click the following link to confirm your registration:
    http://127.0.0.1:8000/activate/{{ uid }}/{{ token }}
    """)

    template.globals['now'] = datetime.datetime.utcnow
    template.globals['user'] = queryset_user.user
    template.globals['uid'] = urlsafe_base64_encode(force_bytes(queryset_user.user.pk))
    template.globals['token'] = account_activation_token.make_token(queryset_user.user)
    message = render_to_string('firstapp/activation_request.html', {
        'user': queryset_user.user,
        'domain': 'http://127.0.0.1:8000/',
        'uid': urlsafe_base64_encode(force_bytes(queryset_user.user.pk)),
        'token': account_activation_token.make_token(queryset_user.user),
    })
    subject = 'Please Activate Your Account'
    queryset_user.user.email_user(subject, template.render())


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'signup_confirmation']
    actions = ['send_signup_confirmation']

    def send_signup_confirmation(self, request, queryset):
        pool = Pool(5)
        pool.map(send, queryset)
    send_signup_confirmation.short_description = "Send signup confirmation"


admin.site.register(Heroes)
admin.site.register(Guide)
admin.site.register(Items)
admin.site.register(Neutrals)
admin.site.register(Role)
admin.site.register(Runes)
admin.site.register(Profile, ProfileAdmin)
