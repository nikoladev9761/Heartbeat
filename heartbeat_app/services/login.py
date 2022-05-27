class LoginService():
	def __init__(self, login_repository):
		self._repo = login_repository

	def login(self, request, username, pswd) -> bool:
		self._repo.login(request, username, pswd)

	def send_recovery_token(self, request, email) -> bool:
		return self._repo.send_recovery_token(request, email)

	def update_pswd(self, request, token, new_pswd):
		self._repo.update_pswd(request, token, new_pswd)