from django.contrib import admin
from .models import User, Title, Comment, Category, Review, Genre, GenreTitle, ConfirmationCode


class TitleAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'year',
		'rating',
		'description',
		'category',
	)
	list_editable = (
		'category',
	)
	search_fields = ('name',)
	list_filter = ('category', 'genre')
	list_display_links = ('name',)


class UserAdmin(admin.ModelAdmin):
	list_display = (
		'username',
		'email',
		'role',
		'first_name',
		'last_name',
		'bio',
		'password',
	)
	list_editable = (
		'role',
	)
	search_fields = ('username',)
	list_display_links = ('username',)


class CategoryAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'slug',
	)
	search_fields = ('name',)
	list_display_links = ('name',)


class ReviewAdmin(admin.ModelAdmin):
	list_display = (
		'text',
		'score',
		'pub_date',
		'author',
		'title',
	)
	search_fields = ('text', 'author')
	list_display_links = ('author',)


class CommentAdmin(admin.ModelAdmin):
	list_display = (
		'text',
		'pub_date',
		'author',
		'review',
	)
	search_fields = ('text', 'author')
	list_display_links = ('author',)


class GenreAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'slug',
	)
	search_fields = ('name',)
	list_display_links = ('name',)


class GenreTitleAdmin(admin.ModelAdmin):
	list_display = (
		'genre',
		'title',
	)
	list_display_links = ('genre', 'title')
	search_fields = ('genre', 'title')
	list_filter = ('genre', 'title')


class ConfirmationCodeAdmin(admin.ModelAdmin):
	list_display = (
		'user',
		'code',
	)


admin.site.empty_value_display = 'Не задано'
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(ConfirmationCode, ConfirmationCodeAdmin)
