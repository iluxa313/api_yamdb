from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_year, validate_slug
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class BaseSlugNameModel(models.Model):
    name = models.TextField('Название', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, validators=[validate_slug, ])

    class Meta:
        abstract = True


class Category(BaseSlugNameModel):

    class Meta:
        ordering = ('id',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(BaseSlugNameModel):

    class Meta:
        ordering = ('id',)
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год', validators=[validate_year,])
    rating = models.IntegerField('Рейтинг', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, verbose_name='Произведение')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')

    class Meta:
        ordering = ('id',)
        verbose_name = 'жанр - произведение'
        verbose_name_plural = 'жанры - произведения'

    def __str__(self):
        return f'Произведение: "{self.title}". Жанр: "{self.genre}"'


class Review(models.Model):
    text = models.TextField('Текст')
    score = models.PositiveSmallIntegerField(
        'Оценка', validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews', verbose_name='Произведение'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return f'Отзыв от {self.author} на произведение "{self.title}"'


class Comment(models.Model):
    text = models.TextField('Текст', max_length=200)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments', verbose_name='Отзыв'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'Комментарий от {self.author} на "{self.review}"'


class ConfirmationCode(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='codes'
    )
    code = models.CharField('Код', max_length=6)

    class Meta:
        verbose_name = 'код подтверждения'
        verbose_name_plural = 'коды подтверждения'

    def __str__(self):
        return self.code
