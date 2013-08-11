from butler.jobs.workflow import Step


class Update(Step):
    def run(self, **context):
        return {}