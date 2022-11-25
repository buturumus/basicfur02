# misc/common_classes.py

class Initable:
    # DEFAULT_KEYSET = (
    #     ('username'),
    #     ('set_password', 'is_staff', 'is_superuser')
    # )
    # DEFAULT_KEYVALS = {
    #     'b3admin': ('b3adminb3admin', True, True),
    #     'test': ('test', True, False),
    #     'empty_key': (),
    # }

    @classmethod
    def check_init_defaults(cls):
        for key_name in cls.DEFAULT_KEYVALS:
            # check if such instance exists
            try:
                uid = cls.objects.get(  # noqa
                    cls.DEFAULT_KEYSET[0], key_name)
                continue
            # if doesn't then create it and fill with data
            except:
                obj = cls()
                setattr(obj, cls.DEFAULT_KEYSET[0], key_name)
                # if there are other non-empty keys
                if cls.DEFAULT_KEYVALS[key_name]:
                    for the_key, the_val in zip(
                        cls.DEFAULT_KEYS[1],
                        cls.DEFAULT_KEYVALS[key_name]
                    ):
                        # N.B. the method
                        # must be set in the model
                        obj.__class__.second_defaults_init_method(
                            obj, the_key, the_val
                        )
                obj.save()

    @classmethod
    def reset_defaults(cls):
        cls.objects.all().delete()
        cls.init_defaults(cls)


class ClassNameGetter:

    @classmethod
    def get_class_name(cls):
        return cls.__name__

    # classname's getting works correct with an instance of a model only
    @staticmethod
    def name_from_model(model):
        try:
            name = model.get_class_name()
            return name
        except AttributeError:
            return ''

