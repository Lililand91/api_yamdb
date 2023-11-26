from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from api.validators import username_validator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User

    def validate_username(self, value):
        return username_validator(value)


class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class SignupSerializer(Serializer):
    username = CharField(
        max_length=settings.LIMIT_USERNAME,
        required=True,
        validators=(username_validator,),
    )
    email = EmailField(max_length=settings.LIMIT_EMAIL, required=True)


class TokenSerializer(Serializer):
    username = CharField(
        max_length=settings.LIMIT_USERNAME,
        required=True,
        validators=(username_validator,),
    )
    confirmation_code = CharField(
        max_length=settings.LIMIT_CODE, required=True
    )

    def validate_username(self, value):
        return username_validator(value)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'rating', 'description', 'genre', 'category',)
        read_only_fields = ('__all__',)

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        return reviews.aggregate(rating=Avg('score')).get('rating')


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'rating', 'description', 'genre', 'category',)

    def validate_year(self, year):
        if year > date.today():
            raise ValidationError('Произведение ещё не вышло.')
        return year


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('product',)


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
