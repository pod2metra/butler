from butler.jobs.orm.django.workflow import ProcessDjangoModel
from butler.resource import DjangoResource
from api.v0_1 import base_workflow
from link_sorter.models import LinkStatistics


class LinkStatisticsResource(DjangoResource):
    workflow = base_workflow.base_wf.replace(
        process_model=ProcessDjangoModel(model_klass=LinkStatistics)
    )

    class Meta:
        model = LinkStatistics
