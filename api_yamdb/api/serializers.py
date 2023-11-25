from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField(max_value=10, min_value=0)

    class Meta:
        model = Title
        fields = ('id', 'name', 'rating', 'description', 'genre', 'category',)

    def get_rating(self, request, obj):
        reviews = Review.objects.filter(product=request.product)
        rating = 0
        for review in reviews:
            rating = rating + review.score
        return rating / len(reviews)
