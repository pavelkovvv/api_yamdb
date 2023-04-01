from django.contrib import admin

from reviews.models import Category, Genre, Title, Review, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'score', 'title')
    empty_value_display = '-пусто-'
    ordering = ('-pk',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'review')
    empty_value_display = '-пусто-'
    ordering = ('-pk',)
    