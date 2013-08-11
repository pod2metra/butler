from butler.jobs.workflow import Step


class AlwaysAuthorizedCheck(Step):
    def run(self, **context):
        return {}


class HasPermissionsCheck(Step):
    def run(self, **context):
        return {}