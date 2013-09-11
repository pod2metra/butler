from butler.jobs.response.simple import WrapResponse
from butler.jobs.serialization.simple import FromString, ToString
from butler.jobs.auth.dummy import AlwaysAuthorizedCheck, HasPermissionsCheck
from butler.jobs.workflow import Workflow, Placeholder


base_wf = Workflow(
    AlwaysAuthorizedCheck(),
    HasPermissionsCheck(),
    FromString(default_format='json'),
    Placeholder('process_model'),
    ToString(default_format='json'),
    WrapResponse()
)
