class NotSuchFileError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'There is no such file as a ' + str(self.value)


class PermissionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'You have not permissions for removing ' + str(self.value)


class NotFileError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value) + ' is not a file or link'


class NotDirectoryError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value) + ' is not a directory'


class RemoveError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Can not remove' + str(self.value)


class TrashSetError(Exception):
    def __init__(self, value):
        self.value = value

    def get_list(self):
        return self.value


class DatabaseSetError(Exception):
    def __init__(self, value):
        self.value = value

    def get_list(self):
        return self.value
