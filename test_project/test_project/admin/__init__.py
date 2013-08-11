from django.contrib import admin
from test_project.models.link import Link
from test_project.models.link_statistic import LinkStatistics

models = (
    Link,
    LinkStatistics,
)

for model in models:
    admin.site.register(model)

