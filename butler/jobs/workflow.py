
class Step(object):
    def __call__(self, request, **context):
        raise self.run(request, **context)

    def run(self, request, **kwargs):
        raise NotImplementedError()


class Placeholder(Step):
    def __init__(self, name):
        self.name = name

    def __call__(self, **context):
        return context


class Workflow(Step):

    def __init__(self, *steps, **kwargs):
        self.steps = steps
        self.kwargs = kwargs

    def __call__(self, **context):
        return self.run(**context)

    def run(self, request, **context):
        for step in self.steps:
            context = step(request, **context)
        return context

    def replace(self, placeholder_name, callable_object):
        steps = []
        for step in self.steps:
            if isinstance(step, Placeholder) and step.name == placeholder_name:
                step = callable_object
            steps.append(step)
        return self.__class__(*steps, **self.kwargs)
