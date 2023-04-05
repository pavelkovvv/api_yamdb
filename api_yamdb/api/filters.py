from django_filters.rest_framework import CharFilter, FilterSet
from titles.models import Title


class TitleFilter(FilterSet):
    """Фильтр полей произведения."""
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name="genre__slug")

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')
