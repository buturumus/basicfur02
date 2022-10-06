# misc/common_classes.py

class Initable:
    # DEFAULT_KEYS = ('username', 'set_password', 'is_staff', 'is_superuser')
    # DEFAULT_VALS = (
    #     ('b3admin', 'b3adminb3admin', True, True),
    #     ('test', 'test', True, False),
    # )

    @classmethod
    def init_defaults(cls):
        for vals_line in cls.DEFAULT_VALS:
            # check if such instance exists
            try:
                uid = cls.objects.get(  # noqa
                    **{cls.DEFAULT_KEYS[0], vals_line[0]})
                continue
            # if doesn't then create it and fill with data
            except:
                obj = cls()
                for key, theval in zip(cls.DEFAULT_KEYS, vals_line):
                    setattr(obj, key, theval)
                obj.save()

    @classmethod
    def reset_defaults(cls):
        cls.objects.all().delete()
        cls.init_defaults(cls)


    
