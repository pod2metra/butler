from butler.jobs.helpers import RequestMethodSwitch, Rename
from butler.jobs.orm.django.steps.create import Create
from butler.jobs.orm.django.steps.filter import ModelFilter
from butler.jobs.orm.django.steps.to_dict import ToDict
from butler.jobs.orm.django.steps.update import Update
from butler.jobs.orm.django.steps.delete import Delete
from butler.jobs.orm.django.steps.limit import Limit
from butler.jobs.workflow import Workflow


class ProcessDjangoModel(RequestMethodSwitch):

    def __init__(self, model_klass, required_filters=None, allowed_fields=None):
        ToDictInstance = ToDict(
            model_klass=model_klass,
            allowed_fields=allowed_fields
        )
        GetModel = Workflow(
            ModelFilter(model_klass),
            Rename('filtered', 'data'),
            Limit(),
            ToDictInstance,
        )
        UpdateModel = Workflow(
            ModelFilter(model_klass),
            Update(model_klass),
        )
        DeleteModel = Workflow(
            ModelFilter(model_klass),
            Delete(),
        )
        CreateModel = Workflow(
            Create(model_klass),
            Rename('created', 'data'),
            ToDictInstance,
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

