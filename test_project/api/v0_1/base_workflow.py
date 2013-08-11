from butler.jobs.serialization.steps import FromString, ToString
from butler.jobs.auth.dummy import AlwaysAuthorizedCheck, HasPermissionsCheck
from butler.jobs.workflow import Workflow, Placeholder

base_wf = Workflow(
    AlwaysAuthorizedCheck(),
    HasPermissionsCheck(),
    FromString(),
    Placeholder('process_model'),
    ToString(),
)
