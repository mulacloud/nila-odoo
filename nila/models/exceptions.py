class BadRequest(Exception):
        def __init__(self, message, code=400, data=None):
            super().__init__(message)
            self.code = code
            self.data = data or {}
