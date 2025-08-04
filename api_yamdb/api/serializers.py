from reviews.models import (User, Category, Genre, Title, GenreTitle,
                            Review, Comment, ConfirmationCode)
from rest_framework import serializers
from django.core.validators import MaxLengthValidator


class MyTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data["username"]
        code = data["confirmation_code"]
        user = User.objects.filter(username=username).first()

        if not user:
            raise serializers.ValidationError(
                {"username": "Не существует такого пользователя."}
            )

        if user.codes.code != code:
            raise serializers.ValidationError(
                {"confirmation_code": "Неверный код подтверждения."}
            )

        data['user'] = user
        return data


class SignUpUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'bio', 'role')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        validators=[MaxLengthValidator(150)]
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        validators=[MaxLengthValidator(150)]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if 'first_name' in data and len(data['first_name']) > 150:
            raise serializers.ValidationError({
                'first_name': 'Максимальная длина поля - 150 символов'
            })
        if 'last_name' in data and len(data['last_name']) > 150:
            raise serializers.ValidationError({
                'last_name': 'Максимальная длина поля - 150 символов'
            })
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        min_value=1,
        max_value=10
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'pub_date')


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_genre(self, value):
        for genre in value:
            if not Genre.objects.filter(slug=genre.slug).exists():
                raise serializers.ValidationError(
                    f'Жанр с slug {genre.slug} не существует'
                )
        return value

    def validate_category(self, value):
        if not Category.objects.filter(slug=value.slug).exists():
            raise serializers.ValidationError(
                f'Категория с slug {value.slug} не существует'
            )
        return value

    def create(self, validated_data):
        genres_data = validated_data.pop('genre', [])
        category_data = validated_data.pop('category', None)

        title = Title.objects.create(**validated_data)

        if category_data:
            title.category = category_data
            title.save()

        for genre in genres_data:
            title.genre.add(genre)

        return title


class TitleReadSerializer(TitleWriteSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        scores = [review.score for review in reviews]
        return round(sum(scores) / len(scores), 1)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'pub_date')
        extra_kwargs = {
            'text': {'required': True}
        }
