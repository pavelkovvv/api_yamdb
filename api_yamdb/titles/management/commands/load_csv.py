import csv

from django.core.management import BaseCommand
from django.conf import settings

from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import User


MODELS = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for model in MODELS:
            with open(
                f'{settings.BASE_DIR}/static/data/{MODELS.get(model)}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('correct upload'))
