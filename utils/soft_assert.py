class SoftAssert:
    def __init__(self):
        self.errors = []

    def check(self, condition, message=""):
        if not condition:
            self.errors.append(message)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.errors:
            raise AssertionError("\n".join(self.errors))
