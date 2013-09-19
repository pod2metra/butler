import logging

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from butler.jobs import exceptions
from butler.jobs.context import Context
from butler.jobs.workflow import Workflow
from butler.meta import InheritedMetaClass
from butler.utils import strings

logger = logging.getLogger(__name__)


class DjangoResource(object):
    __metaclass__ = InheritedMetaClass

    def __init__(self, workflow=None, name=None):
        super(DjangoResource, self).__init__()

        workflow = workflow or self.workflow or self._meta.workflow

        if not workflow:
            raise exceptions.ButlerException('Workflow should be non empty')

        if hasattr(workflow, '__iter__'):
            workflow = Workflow(workflow)

        meta_name = getattr(self._meta, 'name', None)
        if meta_name:
            meta_name = strings.to_underscore(meta_name)

        self.name = name or meta_name or self.__class__.__name__.lower()
        self.workflow = workflow

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        context = Context()
        try:
            context['resource'] = self
            context['request'] = request
            context.update(kwargs)
            context['args'] = args
            return self.workflow.run(**context).get('response')
        except exceptions.ButlerException as e:
            return e.as_response(
                request,
                self,
                context
            )
        except Exception as e:
            logger.exception('some bad things happened')
            return exceptions.ExceptionWrapper(e).as_response(
                request,
                self,
                context
            )

    def get_urls(self, api_name, version):
        return None

    class Meta:
        format = getattr(settings, 'DEFAULT_FORMAT', 'json')
