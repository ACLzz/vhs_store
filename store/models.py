from django.db import models


class Genre(models.Model):

    name = models.CharField(max_length=50)


class Film(models.Model):

    image = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    genres = models.ManyToManyField(Genre)
    actors = models.CharField(max_length=256, null=True)
    description = models.TextField(max_length=1024)
    rate = models.CharField(max_length=5)


class Cassette(models.Model):

    film_id = models.ForeignKey(Film, models.CASCADE)
    cover = models.CharField(max_length=125)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class User(models.Model):

    avatar = models.CharField(max_length=110)
    first_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=25)
    password = models.CharField(max_length=64)
    registration_date = models.DateTimeField(auto_now=True)
    birth_date = models.DateTimeField()
