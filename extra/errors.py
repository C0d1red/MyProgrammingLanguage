class Error:

    def __init__(self, msg, details):
        self.details = details
        self.msg = msg

    def __repr__(self):
        return self.msg + self.details


class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Error on character: ', details)


class InvalidSyntaxError(Error):
    def __init__(self, details):
        super().__init__('Syntax error: ', details)
