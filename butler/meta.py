class InheritedMetaClass(type):
    @staticmethod
    def inherit_meta(bases, dct):
        meta_based = []
        if 'Meta' in dct:
            meta_based.append(dct['Meta'])

        for b in bases:
            if not hasattr(b, '_meta_class'):
                continue

            meta_based.append(b._meta_class)

            if not hasattr(b, '__metaclass__'):
                continue

            dct['__metaclass__'] = b.__metaclass__

        meta_based.append(object)
        meta_class = type('Meta', tuple(meta_based), {})
        dct['_meta_class'] = meta_class
        _meta = meta_class()
        dct['_meta'] = _meta
        return meta_class

    def __new__(cls, name, bases, attrs):
        InheritedMetaClass.inherit_meta(bases, attrs)
        new_class = type.__new__(cls, name, bases, attrs)

        for obj_name, obj in attrs.items():
            if hasattr(obj, 'contribute_to_class'):
                obj.contribute_to_class(obj_name, new_class)

        return new_class



    def __init__(cls, what, bases=None, dict=None):
        super(InheritedMetaClass, cls).__init__(what, bases, dict)
