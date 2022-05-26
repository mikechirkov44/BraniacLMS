from django.core.management import BaseCommand
from mainapp.models import News

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for i in range(10):
            News.objects.create(
                title=f"title#{i}",
                preamble=f"preamble#{i}",
                body=f"some body {i}"
            )


