from django.db import models

from .link import Link


class LinkStatistics(models.Model):
    link = models.ForeignKey(Link)

    # Count of creation requests
    created_count = models.IntegerField(default=0)
    # Count of redirects from short link
    redirect_count = models.IntegerField(default=0)
