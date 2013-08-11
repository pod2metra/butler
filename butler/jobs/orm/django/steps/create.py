from butler.jobs.workflow import Step


class Create(Step):
    def run(self, **context):
        return {}