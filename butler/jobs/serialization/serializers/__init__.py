from butler.jobs.serialization.serializers.js import JsonSerializer
from butler.jobs.serialization.serializers.xml import XMLSerializer
from butler.jobs.serialization.serializers.yaml import YAMLSerializer

registered = {
    'json': JsonSerializer(),
    'xml': XMLSerializer(),
    'yaml': YAMLSerializer()
}