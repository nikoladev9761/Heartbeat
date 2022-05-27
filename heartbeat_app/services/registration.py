class RegistrationService():
	def __init__(self, registration_repository):
		self._repo = registration_repository

	def register(self, request, username, pswd, email):
		return self._repo.register(request, username, pswd, email)	
		
	def account_verification(self, request, token):
		return self._repo.account_verification(request, token)

	