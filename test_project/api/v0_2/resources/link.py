from api.v0_1 import base_workflow
from butler.resource import DjangoResource
from test_project.models import Link


class LinkResource(DjangoResource):
    workflow = base_workflow.base_wf

    class Meta:
        model = Link
