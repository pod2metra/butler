from models.link import Link


class LinkResource(Resource):
    workflow = [
    ]

    class Meta:
        model = Link
