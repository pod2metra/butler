from api.v0_1 import base_workflow
from butler.resource import DjangoResource
from test_project.models import LinkStatistics


class LinkStatisticsResource(DjangoResource):
    workflow = base_workflow.base_wf



    class Meta:
        model = LinkStatistics
