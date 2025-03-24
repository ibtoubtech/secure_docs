from django.core.management.base import BaseCommand
from documents.models import Document

class Command(BaseCommand):
    help = 'Deletes all documents from the database'

    def handle(self, *args, **options):
        count = Document.objects.count()
        Document.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} documents')
        )
