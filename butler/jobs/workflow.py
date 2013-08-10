from django.http import HttpResponse
from butler.jobs.exceptions import ButlerException


class Step(object):
    def __call__(self, **context):
        raise self.run(**context)

    def run(self, **context):
        raise NotImplementedError()


class Placeholder(Step):
    def __init__(self, name):
        self.name = name

    def __call__(self, **kwargs):
        return kwargs


class NoStepsSpecified(ButlerException):

    def as_response(self, request, resource, context):
        error = 'No steps for {} resource specified.'.format(
            resource.name
        )
        return HttpResponse(
            content=error
        )


class Workflow(Step):

    def __init__(self, *steps, **kwargs):
        self.steps = steps
        self.kwargs = kwargs

    def __call__(self, **context):
        return self.run(**context)

    def run(self, **context):
        if not self.steps:
            raise NoStepsSpecified(context.get('resource'))

        for step in self.steps:
            context.update(step(**context))

        return context

    def replace(self, placeholder_name, callable_object):
        steps = []
        for step in self.steps:
            if isinstance(step, Placeholder) and step.name == placeholder_name:
                step = callable_object
            steps.append(step)
        return self.__class__(*steps, **self.kwargs)