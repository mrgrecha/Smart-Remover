class Policy(object):
    def run(self, trash):
        raise NotImplementedError()

    def update(self, trash):
        raise NotImplementedError()
