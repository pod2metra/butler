from api.v0_1 import base_workflow
from butler.jobs.orm.django.workflow import ProcessDjangoModel
from butler.resource import DjangoResource
from test_project.models import Link


class LinkResource(DjangoResource):
    workflow = base_workflow.base_wf.replace(
        process_model=ProcessDjangoModel(model_klass=Link)
    )

    class Meta:
        model = Link
