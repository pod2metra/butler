from django.db import models

from django.conf import settings


class Link(models.Model):
    long_link = models.URLField()
    created_at = models.DateTimeField(auto_created=True)

    @property
    def short_link(self):
        short_link = hex(self.pk)[2:]
        return '{}/{}'.format(settings.SHORTER_STARTER_LINK, short_link)


class LinkStatistics(models.Model):
    link = models.ForeignKey(Link)

    # Count of creation requests
    created_count = models.IntegerField(default=0)
    # Count of redirects from short link
    redirect_count = models.IntegerField(default=0)
