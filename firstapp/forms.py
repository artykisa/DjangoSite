from django import forms
from django.forms import ModelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Heroes, Guide


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
