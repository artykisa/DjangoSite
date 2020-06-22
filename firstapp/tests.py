from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
import uuid
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import Heroes, Guide, Role, Profile, Runes, Neutrals
from .tokens import account_activation_token


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('rocky', 'bumbini@gmail.com', 'password')
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_unauthorized(client):
    response = client.get('/admin/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_superuser_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_detail(client, django_user_model):
    django_user_model.objects.create_user(username='someone', password='password')
    client.login(username='someone', password='password')
    url = reverse('profile')
    response = client.get(url)
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_guide_update(client, django_user_model):
#     django_user_model.objects.create_user(username='someone', password='password')
#     client.login(username='someone', password='password')
#     rune = Runes(name='Electrocute', code='r45434babc44')
#     sums = Summoners(name='Flash', code=69)
#     role = Role(lane='jungle')
#     champ = Champion(name='Lee', picture='lee.jpg')
#     rune.save()
#     sums.save()
#     role.save()
#     champ.save()
#     mp = Guide(id=1, champion=champ, build_skill='qqqqqqqqqqqqqqqq', build_runes=rune, build_summoners=sums, role=role)
#     mp.save()
#     url = reverse('guide_update', kwargs={'pk': 1})
#     response = client.get(url)
#     assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("username, status_code", [
    ("someone", 200),
    ("someone2", 200)
])
def test_register(client, django_user_model, username, status_code):
    django_user_model.objects.create_user(username=username, password='password')
    client.login(username=username, password='password')
    url = reverse('profile')
    response = client.get(url)
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_guide_delete(client, django_user_model):
#     django_user_model.objects.create_user(username='someone', password='password')
#     client.login(username='someone', password='password')
#     rune = Runes(name='Electrocute', code='r45434babc44')
#     sums = Summoners(name='Flash', code=69)
#     role = Role(lane='jungle')
#     champ = Champion(name='Lee', picture='lee.jpg')
#     rune.save()
#     sums.save()
#     role.save()
#     champ.save()
#     mp = Guide(id=1, champion=champ, build_skill='qqqqqqqqqqqqqqqq', build_runes=rune, build_summoners=sums, role=role)
#     mp.save()
#     url = reverse('delete', kwargs={'pk': 1})
#     response = client.get(url)
#     assert response.status_code == 200


@pytest.mark.django_db
def test_guide_add(client, django_user_model):
    django_user_model.objects.create_user(username='someone', password='password')
    client.login(username='someone', password='password')
    url = reverse('guide_new')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_view(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_5(client):
    response = client.get('/fivexfive/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_4(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_3(client):
    response = client.get('/fivexfive/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_0(client):
    response = client.get('/register/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_10(client):
    response = client.get('/logout/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_1(client):
    response = client.get('/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_contact(client):
    response = client.get('/contact/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_2(client):
    response = client.get('/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_4(client):
    response = client.get('/articles/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_5(client):
    response = client.get('/guides/')
    assert response.status_code == 200


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


@pytest.mark.django_db
def test_auth_view(auto_login_user):
    client, user = auto_login_user()
    response = client.get('/register/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_guideop_view(auto_login_user):
    client, user = auto_login_user()
    response = client.get(
        '/guides/cur_guide/?name=Terrorblade&role=Mid(2)&build_runes=bounty&build_opa=invis&build_jopa=arcane&build_skill=313134311224224&build_sum=1&build_sum2=17&build_sum3=31&build_sum4=39&build_sum5=45&build_items=refr&build_items2=mek&build_items3=guard&build_items4=refr&build_items5=guard')
    assert response.status_code == 200


@pytest.mark.django_db
def test_activate_view(auto_login_user):
    client, user = auto_login_user()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    url = reverse('activate', args=[uid, token])
    response = client.get(url)
    assert response.status_code == 200
