from logging import Logger
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm, GuideAddForm, ArticleForm, SignUpForm
from .models import Heroes, Guide
import logging.config
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView
from .forms import UserRegisterForm, Profile, ProfileForm, EditUserForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from djangolab.settings import LOGGING
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .tokens import account_activation_token
import logging.config


# Create your views here.


logging.config.dictConfig(LOGGING)
logger: Logger = logging.getLogger(__name__)


class MemberList(ListView):
    model = Heroes


class GuideList(ListView):
    model = Guide


def guide(request):
    name, role, build_runes, build_skill, build_sum, build_opa, build_jopa, build_sum2, build_sum3, build_sum4, build_sum5, build_items, build_items2, build_items3, build_items4, build_items5 = request.GET.get(
        "name", "noname"), request.GET.get("role", "norole"), request.GET.get("build_runes", "0"), request.GET.get(
        "build_skill", "0"), request.GET.get("build_sum", "0"), request.GET.get("build_opa", "0"), request.GET.get(
        "build_jopa", "0"), request.GET.get("build_sum2", "0"), request.GET.get("build_sum3", "0"), request.GET.get(
        "build_sum4", "0"), request.GET.get("build_sum5", "0"), request.GET.get("build_items", "0"), request.GET.get(
        "build_items2", "0"), request.GET.get("build_items3", "0"), request.GET.get("build_items4", "0"), request.GET.get("build_items5", "0")
    build_skill = build_skill.upper()
    data = {
        'name': name,
        'build_runes': build_runes,
        'build_skill': build_skill,
        'build_sum': '',
        'build_sum_link1': "images/" + build_sum + ".png",
        'build_sum_link2': "images/" + build_sum2 + ".png",
        'build_sum_link3': "images/" + build_sum3 + ".png",
        'build_sum_link4': "images/" + build_sum4 + ".png",
        'build_sum_link5': "images/" + build_sum5 + ".png",
        'build_runes_link1': "images/" + build_runes + ".png",
        'build_runes_link2': "images/" + build_opa + ".png",
        'build_runes_link3': "images/" + build_jopa + ".png",
        'build_items_link1': "images/" + build_items + ".png",
        'build_items_link2': "images/" + build_items2 + ".png",
        'build_items_link3': "images/" + build_items3 + ".png",
        'build_items_link4': "images/" + build_items4 + ".png",
        'build_items_link5': "images/" + build_items5 + ".png",
        'role': role,
    }
    return render(request, "firstapp/guide.html", context=data)


def account(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            user_form = EditUserForm(initial={
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            })
            profile_form = ProfileForm(initial={
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'signup_confirmation': request.user.profile.signup_confirmation,
            })
            context = {'profile_form': profile_form}
            return render(request, 'firstapp/profile.html', context)
    else:
        user_form = EditUserForm(initial={
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'signup_confirmation': request.user.profile.signup_confirmation,
        })
        profile_form = ProfileForm(initial={
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'signup_confirmation': request.user.profile.signup_confirmation,
            }
        )
    context = {
        'profile_form': profile_form
    }
    return render(request, 'firstapp/profile.html', context)


def register(request):
    print("123")
    logger.info("attempt to signup")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('firstapp/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return render(request, 'firstapp/activation_sent.html')
    else:
        form = SignUpForm()
    return render(request, 'firstapp/register.html', {'form': form})


def activation_sent_view(request):
    logger.debug("activation sent")
    return render(request, 'firstapp/activation_sent.html')


def champion(request):
    data = Heroes.objects.values()
    context = {}

    for element in data:
        list = [element.name, element.picture]
        context.update({element.id: list})
    return render(request, "firstapp/heroes_list.html", context=context)


def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        return HttpResponse("<h2>Hello, {0}</h2>".format(name))
    else:
        userform = UserForm()
        return render(request, "firstapp/login.html", {"form": userform})


def add_guide(request):
    return render(request, GuideAddForm.as_view())


class GuideCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': GuideAddForm()}
        return render(request, 'firstapp/guide_form.html', context)

    def post(self, request, *args, **kwargs):
        form = GuideAddForm(request.POST)
        if form.is_valid():
            cur_guide = form.save()
            cur_guide.save()
            return render(request, 'firstapp/guide_list.html')
        return render(request, 'firstapp/guide_form.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        logger.debug("activation")
        return render(request, 'firstapp/main.html')
    else:
        logger.debug("activation fail")
        return render(request, 'activation_invalid.html')


def about(request):
    return HttpResponse("<h2>О сайте</h2>")


def contact(request):
    return HttpResponse("<h2>Контакты</h2>")


def products(request, productid=0):
    category = request.GET.get("cat", "")
    output = "<h2>Product № {0} Category: {1}</h2>".format(productid, category)
    return HttpResponse(output)


def users(request, id=0, name="Noname"):
    id = request.GET.get("id", 1)
    name = request.GET.get("name", "Tom")
    output = "<h2>User</h2><h3>id: {0} name:{1}</h3>".format(id, name)
    return HttpResponse(output)
