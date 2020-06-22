from django import forms
from django.forms import ModelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Heroes, Guide, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ArticleForm(ModelForm):
    class Meta:
        model = Guide
        fields = ['heroes', 'role']


class UserForm(forms.Form):
    name = forms.CharField(label="Имя", initial="undefiend")
    age = forms.IntegerField(label="Возраст", initial=18)
    comment = forms.CharField(label="Комментарий", widget=forms.Textarea, required=False)


class GuideAddForm(CreateView):
    model = Guide
    fields = ('heroes', 'build_skill', 'build_items', 'build_items2', 'build_items3', 'build_items4', 'build_items5',
              'build_runes', 'build_opa', 'build_jopa', 'build_neutrals', 'build_neutrals2',
              'build_neutrals3', 'build_neutrals4', 'build_neutrals5', 'role')

    success_url = "/"


class GuideUpdateForm(UpdateView):
    model = Guide
    fields = ['heroes', 'build_skill', 'build_items', 'build_items2', 'build_items3', 'build_items4', 'build_items5',
              'build_runes', 'build_opa', 'build_jopa', 'build_neutrals', 'build_neutrals2',
              'build_neutrals3', 'build_neutrals4', 'build_neutrals5', 'role']

    template_name_suffix = '_update_form'
    success_url = "/"


class GuideDeleteForm(DeleteView):
    model = Guide
    fields = ['heroes', 'build_skill', 'build_items', 'build_items2', 'build_items3', 'build_items4', 'build_items5',
              'build_runes', 'build_opa', 'build_jopa', 'build_neutrals', 'build_neutrals2',
              'build_neutrals3', 'build_neutrals4', 'build_neutrals5', 'role']

    template_name_suffix = '_delete_form'
    success_url = "/"


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email',
                  'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditUserForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'signup_confirmation']
