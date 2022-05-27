from heartbeat_app.models import User
from .security import SecurityRepo
from django.contrib import messages
from .emails import EmailRepo
from .notification import NotificationRepo

notification = NotificationRepo()


class LoginRepo():

	def login(self, request, username, pswd):
		login_validation = SecurityRepo().validate_login(username, pswd)
		
		if login_validation == True:
			try:
				user_data = User.objects.values('id', 'pswd').filter(username = username, emailVerified = True)
				get_id = user_data[0].get('id')
				hashed_pswd = user_data[0].get('pswd')
				penalty_exists = SecurityRepo().check_penalty(username)
				
				if penalty_exists == None:
					try:
						SecurityRepo().password_verify(hashed_pswd, pswd)
						User.objects.filter(id = get_id).update(loginTries = 0, penaltyExpirationDate = None, online = True)
						request.session['user_id'] = get_id
					except:
						get_current_tries = SecurityRepo().login_tries(username)
						SecurityRepo().login_brute_force_protection(get_current_tries, username)
						messages.add_message(request, messages.ERROR, "Credentials incorrect! Try again.")
							
				else:
					notification.generate_status_message(request, 'error', "This user has login penalty!")

			except IndexError:
				notification.generate_status_message(request, 'error', "User doesn't exist! Try again.")
				

	def send_recovery_token(self, request, email):
		token = SecurityRepo().generate_token()
		validate_email = SecurityRepo().validate_recovery_email(email)
		email_sent = True

		if validate_email == True:
			try:
				User.objects.values('email').filter(email = email)[0].get('email')
				User.objects.filter(email = email).update(emailToken = token)
				EmailRepo().send_email_verification(email, token)
				notification.generate_status_message(request, 'success', "Token sent to email.")
			except IndexError:
				email_sent = False
				notification.generate_status_message(request, 'error', "Account with that email doesn't exist!")
				
		else:
			notification.generate_status_message(request, 'error', "Email format invalid!")
		
		return email_sent


	def update_pswd(self, request, token, new_pswd):
		try:
			update_pswd = SecurityRepo().password_hash(new_pswd)
			User.objects.filter(emailToken = token).update(pswd = update_pswd)
			notification.generate_status_message(request, 'success', "New password updated! You can now login.")
		except IndexError:
			notification.generate_status_message(request, 'error', "Invalid token! Check your email again.")