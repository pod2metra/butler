import yaml


class YAMLSerializer(object):
    def to_string(self, data):
        return yaml.dump(data)

    def from_string(self, str_data):
        return yaml.load(str_data)
