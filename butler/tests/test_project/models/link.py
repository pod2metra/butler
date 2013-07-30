from django.db import models

from butler.future.tests.test_project import settings


class Link(models.Model):
    long_link = models.URLField(editable=False)
    created_at = models.DateTimeField(auto_created=True)

    @property
    def short_link(self):
        short_link = hex(self.pk)[2:]
        return '{}/{}'.format(settings.SHORTER_STARTER_LINK, short_link)
