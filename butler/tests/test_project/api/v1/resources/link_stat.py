from butler.future.resource import Resource
from butler.future.tests.test_project.models.link import Link


class LinkStatistics(Resource):
    workflow = wf.set('pizda', ModelProcessing())

    class Meta:
        model = Link
