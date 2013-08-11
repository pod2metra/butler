import xmldict


class XMLSerializer(object):
    content_type = 'application/xml'

    ITEM_TAG = 'item'

    def to_string(self, data):
        serialize_data_dict = {}
        for k, v in data.viewitems():
            if isinstance(v, (list, tuple, set)):
                v = {self.ITEM_TAG: v}
            elif isinstance(v, str):
                v = v.decode('utf-8')
            serialize_data_dict[k] = v
        return xmldict.dict_to_xml({
            'root': serialize_data_dict
        })

    def from_string(self, str_data):
        load_dict = xmldict.xml_to_dict(
            str_data
        ).get('root', {})
        result_dict = {}

        for k, v in load_dict.viewitems():
            if isinstance(v, dict) and [self.ITEM_TAG] == v.keys():
                v = v.values()[0]
            result_dict[k] = v

        for k, v in result_dict.viewitems():
            if v in ['true', 'false']:
                result_dict[k] = v == 'true'

        return result_dict
