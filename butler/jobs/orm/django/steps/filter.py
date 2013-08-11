from butler.jobs.workflow import Step


class Filter(Step):
    def run(self, **context):
        return {}