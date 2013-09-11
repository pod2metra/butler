from api import v0_1
from api.v0_2 import resources
from butler.api import Api

import resources

api = Api(
    'internal',
    'v0.2',
    resources=[
        resources.LinkResource()
    ],
    inherits=v0_1.api
)