from api.v0_1 import resources

from butler.api import Api

api = Api(
    'internal',
    'v0.1',
    resources=[
        resources.LinkResource(name='link'),
        resources.LinkStatisticsResource(name='link_stat')
    ]
)
