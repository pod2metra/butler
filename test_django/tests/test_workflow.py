from unittest import skip
from butler.jobs.workflow import Step
from butler.tests.rest_test import RestResourceTest


class TestStep1(Step):
    def __call__(self, **context):
        return super(TestStep1, self).__call__(**context)


@skip('Not ready yet')
class WorkflowTest(RestResourceTest):

    def test_link_getter(self):
        self.get('/internal/v0.1/link/')
