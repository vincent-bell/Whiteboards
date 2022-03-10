class SecurityError(Exception):
	def __init__(self, message):
		super().__init__(message)


class SetupError(Exception):
	def __init__(self, message):
		super().__init__(message)