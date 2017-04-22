def dry_run(func):
    """
    Dry run decorator
    :param func:
    :return:
    """
    def func_wrapper(self, *args, **kwargs):
        if self.dried:
            pass
        else:
            return func(self, *args, **kwargs)
    return func_wrapper
