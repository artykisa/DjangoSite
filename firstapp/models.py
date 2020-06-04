from django.db import models

# Create your models here.


class Menu(models.Model):
    name=models.CharField(max_length=15)
    url=models.CharField(max_length=15)


class Heroes(models.Model):
    name = models.CharField(max_length=20)
    picture = models.CharField(max_length=24)

    def __str__(self):
        return self.name


class Role(models.Model):
    lane = models.CharField(max_length=20)

    def __str__(self):
        return self.lane


class Neutrals(models.Model):
    name = models.CharField(max_length=15)
    code = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Items(models.Model):
    name = models.CharField(max_length=25)
    code = models.CharField(max_length=18,default='type smth')

    def __str__(self):
        return self.name


class Runes(models.Model):
    name = models.CharField(max_length=25)
    code = models.CharField(max_length=18, default='type smth')

    def __str__(self):
        return self.name


class Guide(models.Model):
    heroes = models.ForeignKey(Heroes, on_delete=models.CASCADE)
    build_skill = models.CharField(max_length=18)
    build_runes = models.ForeignKey(Runes, on_delete=models.CASCADE)
    build_opa = models.ForeignKey(Runes, on_delete=models.CASCADE, related_name='opa', default=None)
    build_jopa = models.ForeignKey(Runes, on_delete=models.CASCADE, related_name='jopa', default=None)
    build_neutrals = models.ForeignKey(Neutrals, on_delete=models.CASCADE, default=None)
    build_neutrals2 = models.ForeignKey(Neutrals, on_delete=models.CASCADE, related_name='neutrals2', default=None)
    build_neutrals3 = models.ForeignKey(Neutrals, on_delete=models.CASCADE, related_name='neutrals3', default=None)
    build_neutrals4 = models.ForeignKey(Neutrals, on_delete=models.CASCADE, related_name='neutrals4', default=None)
    build_neutrals5 = models.ForeignKey(Neutrals, on_delete=models.CASCADE, related_name='neutrals5', default=None)
    build_items = models.ForeignKey(Items, on_delete=models.CASCADE, default=None)
    build_items2 = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='items2', default=None)
    build_items3 = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='items3', default=None)
    build_items4 = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='items4', default=None)
    build_items5 = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='items5', default=None)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


