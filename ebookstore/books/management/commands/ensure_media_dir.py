import os
import stat

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ensure media directories exist with proper permissions (755)."

    # Subdirectories that match the upload_to paths used by models:
    #   books/  — Book.cover  (ImageField)
    #   books/pdfs/  — Book.pdf_file  (FileField)
    #   profiles/  — Profile.image  (ImageField)
    SUBDIRS = [
        "",           # MEDIA_ROOT itself
        "books",
        "books/pdfs",
        "profiles",
    ]

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        created = []
        already_existed = []

        for subdir in self.SUBDIRS:
            path = os.path.join(media_root, subdir) if subdir else media_root
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                created.append(path)
            else:
                already_existed.append(path)

            # Ensure permissions are 755 regardless of whether we just created it
            os.chmod(
                path,
                stat.S_IRWXU  # owner: rwx
                | stat.S_IRGRP | stat.S_IXGRP  # group: r-x
                | stat.S_IROTH | stat.S_IXOTH,  # other: r-x
            )

        for path in created:
            self.stdout.write(self.style.SUCCESS(f"Created:  {path}"))
        for path in already_existed:
            self.stdout.write(f"Exists:   {path}")

        self.stdout.write(self.style.SUCCESS("Media directories are ready."))
