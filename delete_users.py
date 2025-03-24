import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_docs_project.settings')
django.setup()

from django.contrib.auth.models import User
from documents.models import Document

# Delete all documents first
print("Deleting all documents...")
Document.objects.all().delete()

# Delete all users except superuser
print("Deleting all non-superuser accounts...")
User.objects.filter(is_superuser=False).delete()

print("Deletion completed successfully!")
