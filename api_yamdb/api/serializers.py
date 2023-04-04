from django.db.models import Avg
from rest_framework import serializers
from django.core.validators import RegexValidator

from users.models import User
from titles.models import Genre, Category, Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        exclude = ('id',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        exclude = ('id',)
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведения."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('id',)


class GetTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))
        return rating.get('score__avg')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Username должен иметь отличное значение от "me"'
            )
        return data


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Неккоректно введён <username>',
            code='invalid_username'
        )
    ],
        max_length=150
    )

    class Meta:
        model = User
        fields = ('email', 'username')


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)
