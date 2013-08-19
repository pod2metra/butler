from butler.jobs.workflow import Step


class RequestMethodSwitch(Step):
    def __init__(self, methods_workflow):
        super(RequestMethodSwitch, self).__init__()
        self.switch = {}
        for method, workflow in methods_workflow.iteritems():
            self.switch[method.lower()] = workflow

    def run(self, **context):
        request = context.get('request', None)

        if not request:
            return {}

        method = request.method.lower()

        workflow = self.switch.get(method)
        if not workflow:
            return {}

        return workflow(**context)


class Rename(Step):
    def __init__(self, source_name, target_name):
        super(Rename, self).__init__()
        self.source_name = source_name
        self.target_name = target_name

    def run(self, **context):
        return {
            self.target_name: context.get(self.source_name)
        }

