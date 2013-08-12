from butler.jobs.helpers import RequestMethodSwitch
from butler.jobs.orm.django.steps.create import Create
from butler.jobs.orm.django.steps.filter import Filter
from butler.jobs.orm.django.steps.to_dict import ToDict
from butler.jobs.orm.django.steps.update import Update
from butler.jobs.orm.django.steps.delete import Delete
from butler.jobs.workflow import Workflow, Step


class ProcessDjangoModel(RequestMethodSwitch):

    def __init__(self, model_klass, required_filters=None, allowed_fields=None):
        GetModel = Workflow(
            Filter(model_klass),
            ToDict(),
        )
        UpdateModel = Workflow(
            Filter(model_klass),
            Update(),
        )
        DeleteModel = Workflow(
            Filter(model_klass),
            Delete(),
        )
        CreateModel = Workflow(
            Create()
        )
        super(ProcessDjangoModel, self).__init__({
            'get': GetModel,
            'put': UpdateModel,
            'delete': DeleteModel,
            'post': CreateModel
        })
        self.model_klass = model_klass
        self.required_filters = required_filters
        self.allowed_fields = allowed_fields

