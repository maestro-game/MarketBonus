import os

from django.core.management import BaseCommand

from ...models import Director


class Command(BaseCommand):
    help = "Add admin"


    def handle(self, *args, **options):
        if not Director.objects.filter(username=os.getenv('ADMIN_NAME')).exists():
            Director.objects.create_superuser(username=os.getenv('ADMIN_NAME'), password=os.getenv('ADMIN_PASSWORD'))