from datetime import date
from django.db import models

from django.core.exceptions import ValidationError


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:15]


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.TextField('Название', max_length=256)
    yaer = models.DateTimeField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              null=True, related_name='genres')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='categories')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def validate_year(self):
        if self.year > date.today():
            raise ValidationError('Произведение ещё не вышло.')

    def __str__(self):
        return self.name[:15]
