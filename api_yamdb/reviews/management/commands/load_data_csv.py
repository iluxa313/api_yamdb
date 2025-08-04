import csv
from django.core.management.base import BaseCommand
from reviews.models import (User, Category, Genre, Title,
                            Review, Comment, GenreTitle)
from pathlib import Path

class Command(BaseCommand):
    help = 'Загружает книги из CSV в базу данных'

    def handle(self, *args, **options):
        data_path = Path('static/data/')

        file_order = [
            'users.csv',
            'category.csv',
            'genre.csv',
            'titles.csv',
            'genre_title.csv',
            'review.csv',
            'comments.csv'
        ]

        if not data_path.exists():
            self.stderr.write(f'Файл {file_path} не найден.')
            return


        for filename in file_order:
            file_path = data_path / filename
            if not file_path.exists():
                self.stderr.write(f'⚠️ Файл {filename} не найден, пропускаю.')
                continue

            self.stdout.write(f'\nОбработка файла: {filename}')
            count = 0
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                if 'users' in filename:
                    for row in reader:
                        obj, created = User.objects.get_or_create(
                            id=int(row['id']),
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                        )
                        count += 1
                elif 'category' in filename:
                    for row in reader:
                        obj, created = Category.objects.get_or_create(
                            id=int(row['id']),
                            name=row['name'],
                            slug=row['slug']
                        )
                        count += 1
                elif 'genre.csv' in filename:
                    for row in reader:
                        obj, created = Genre.objects.get_or_create(
                            id=int(row['id']),
                            name=row['name'],
                            slug=row['slug']
                        )
                        count += 1
                elif 'titles' in filename:
                    for row in reader:
                        obj, created = Title.objects.get_or_create(
                            id=int(row['id']),
                            name=row['name'],
                            year=int(row['year']),
                            category_id=int(row['category']),
                        )
                        count += 1
                elif 'genre_title' in filename:
                    for row in reader:
                        obj, created = GenreTitle.objects.get_or_create(
                            id=int(row['id']),
                            title_id=int(row['title_id']),
                            genre_id=int(row['genre_id']),
                        )
                        count += 1
                elif 'review' in filename:
                    for row in reader:
                        obj, created = Review.objects.get_or_create(
                            id=int(row['id']),
                            title_id=int(row['title_id']),
                            text=row['text'],
                            author_id=int(row['author']),
                            score=row['score'],
                            pub_date=row['pub_date']
                        )
                        count += 1
                elif 'comments' in filename:
                    for row in reader:
                        obj, created = Comment.objects.get_or_create(
                            id=int(row['id']),
                            review_id=int(row['review_id']),
                            text=row['text'],
                            author_id=row['author'],
                            pub_date=row['pub_date']
                        )
                        count += 1

                self.stdout.write(self.style.SUCCESS(f'Импортировано {count} записей.'))
