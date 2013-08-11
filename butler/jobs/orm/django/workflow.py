from butler.jobs.orm.django.steps.create import Create
from butler.jobs.orm.django.steps.filter import Filter
from butler.jobs.orm.django.steps.update import Update
from butler.jobs.orm.django.steps.delete import Delete
from butler.jobs.workflow import Workflow, Step


class ProcessDjangoModel(Step):

    def __init__(self, model_klass, required_filters=None, allowed_fields=None):
        super(ProcessDjangoModel, self).__init__()
        self.model_klass = model_klass
        self.required_filters = required_filters
        self.allowed_fields = allowed_fields

        GetModel = Workflow(
            Filter(),
        )

        UpdateModel = Workflow(
            Filter(),
            Update(),
        )

        DeleteModel = Workflow(
            Filter(),
            Delete(),
        )

        CreateModel = Workflow(
            Create()
        )

        self.switch = {
            'GET': GetModel,
            'POST': CreateModel,
            'DELETE': DeleteModel,
            'PUT': UpdateModel,
        }

    def run(self, request, resource, **context):
        workflow = self.switch[request.method]

        if not workflow:
            # TODO: normal exception
            raise Exception('Unknown WF')

        return workflow.run()