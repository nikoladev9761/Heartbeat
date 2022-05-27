from heartbeat_app.models import User
from .security import SecurityRepo
from .emails import EmailRepo
from django.db.models import Q
from .notification import NotificationRepo

notification = NotificationRepo()


class RegistrationRepo():

	def register(self, request, username, pswd, email):
		input_validation = SecurityRepo().validate_registration(username, pswd, email)
		
		if input_validation == True:
			try:
				User.objects.values('id').filter(Q(username = username) | Q(email = email))[0]
				notification.generate_status_message(request, 'error', "User with that username/email already exists! Choose another.")
			except IndexError:
				hashedPswd = SecurityRepo().password_hash(pswd)
				token = SecurityRepo().generate_token()
				send_email_confirmation = EmailRepo().send_email_verification(email, token)

				if send_email_confirmation == True:
					notification.generate_status_message(request, 'success', "Registration successful. Confirmation email sent.")
					User(username = username, pswd = hashedPswd, email = email, emailToken = token).save()


	def account_verification(self, request, token):
		token_validation = SecurityRepo().validate_token(token)
		
		if token_validation == True:
			try:
				already_verified = User.objects.filter(emailToken = token, emailVerified = True)
				if already_verified:
					notification.generate_status_message(request, 'info', "Your email is already verified.")
				else:
					get_matching_id = User.objects.values('id').filter(emailToken = token)[0].get('id')
					User.objects.filter(id = get_matching_id).update(emailVerified = True)
					User.objects.filter(id = get_matching_id).update(emailToken = '')	
					notification.generate_status_message(request, 'success', "Verification successful. You can now login.")
			except IndexError:
				notification.generate_status_message(request, 'error', "Invalid token! Please check your email again.")	