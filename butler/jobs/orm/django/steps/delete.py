from butler.jobs.workflow import Step


class Delete(Step):

    def run(self, request, filtered, data, **context):
        count = data.delete()
        return {
            "data": {
                "deleted": count
            }
        }