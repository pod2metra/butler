import logging

from django.conf import settings

from butler.future.jobs import exceptions
from butler.future.jobs.context import Context
from butler.future.jobs.workflow import Workflow

logger = logging.getLogger(__name__)


class Resource(object):
    def __init__(self, workflow=None, name=None):
        super(Resource, self).__init__()

        workflow = workflow or self.workflow or self._meta.workflow

        if not workflow:
            raise exceptions.ButlerException('Workflow should be non empty')

        if hasattr(workflow, '__iter__'):
            workflow = Workflow(workflow)

        self.name = name or self.__class__.__name__.lower()
        self.workflow = workflow

    def dispatch(self, request, *args, **kwargs):
        context = Context()
        context['request'] = request
        try:
            return self.workflow.run(context)
        except exceptions.ButlerResponseException as e:
            return e.as_response(context)
        except Exception as e:
            logger.exception('some bad things happend')
            return exceptions.ButlerErrorResponce(e).as_response(context)

    def get_urls(self, api_name, version):
        return None

    class Meta:
        format = getattr(settings, 'DEFAULT_FORMAT', 'json')
