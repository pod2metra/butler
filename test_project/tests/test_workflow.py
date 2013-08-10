from django import test
from butler.jobs.workflow import Workflow, Step


class TestStep1(Step):
    def __call__(self, **context):
        return super(TestStep1, self).__call__(**context)


class WorkflowTest(test.TestCase):

    def test_shit(self):
        self.assertFalse(True)