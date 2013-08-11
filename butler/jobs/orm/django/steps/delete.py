from butler.jobs.workflow import Step


class Delete(Step):
    def run(self, **context):
        return {}