from django.http import HttpResponse
from butler.tests.test_butler_project.models import Link
from butler.future.jobs.workflow import Workflow, Placeholder
from butler.future.resource import Resource


base_wf = Workflow(
    Placeholder('some_work'),
    resp_creator,
)


def get_link(request, **context):
    return context


class LinkResource(Resource):
    workflow = base_wf.replace('some_work', get_link)

    class Meta:
        model = Link
