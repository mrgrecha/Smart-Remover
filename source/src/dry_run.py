def dry_run(func):
    def func_wrapper(self, *args, **kwargs):
        if self.dried:
            pass
        else:
            return func(self, *args, **kwargs)
    return func_wrapper
