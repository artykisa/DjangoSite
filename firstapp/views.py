from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm, GuideAddForm, ArticleForm
from .models import Heroes, Guide
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView


# Create your views here.


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
        "build_items2", "0"), request.GET.get("build_items3", "0"), request.GET.get("build_items4", "0"), request.GET.get(
        "build_items5", "0")
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
