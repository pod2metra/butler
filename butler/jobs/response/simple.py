from django.http import HttpResponse
from butler.jobs.workflow import Step


class WrapResponse(Step):
    def run(self, **context):
        response_kwargs = {
            'content': context.get('result', None),
            'status': context.get('status_code', 200),
        }
        content_type = context.get('content_type', None)
        if content_type:
            response_kwargs = content_type

        return {
            'response': HttpResponse(**response_kwargs)
        }