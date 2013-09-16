from butler.jobs.workflow import Step


class Delete(Step):


    def __init__(self, return_deleted_count=True):
        super(Delete, self).__init__()
        self.return_deleted_count = return_deleted_count

    def run(self, request, filtered, **context):
        if self.return_deleted_count:
            count = filtered.count()
        else:
            count = True

        filtered.delete()
        return {
            "data": {
                "deleted": count or 0
            }
        }