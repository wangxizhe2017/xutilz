class PostInit(type):
    """
    this class is to activate a post function after __init__() of a class
    """
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.__post_init__()
        return obj

