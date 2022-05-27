from heartbeat_app.models import User, Meeting, MeetingLog
from argon2 import PasswordHasher
import string, random
from re import search
from datetime import datetime, timedelta
from django.utils import timezone
from .notification import NotificationRepo

notification = NotificationRepo()

class SecurityRepo():

	# ----------------------------------- VALIDATION ---------------------------------------------
	def validate_registration(self, username, pswd, email):
		check_usrname = bool(search(r"^[A-Za-z0-9]+$", username))
		check_email = bool(search(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email))
		check_pswd = bool(search(r'\d', pswd))
		if False in {check_usrname, check_email, check_pswd} or len(pswd) < 12:
			return False
		else:
			return True


	def validate_recovery_email(self, email):
		check_email = bool(search(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email))
		if False in {check_email}:
			return False
		else:
			return True


	def validate_token(self, token):
		check_token = bool(search(r"^[A-Za-z0-9]+$", token))
		if False in {check_token} or len(token) != 12:
			return False
		else:
			return True


	def validate_login(self, username, pswd):
		check_usrname = bool(search(r"^[A-Za-z0-9]+$", username))
		check_pswd = bool(search(r'\d', pswd))
		if False in {check_usrname, check_pswd} or len(pswd) < 12:
			return False
		else:
			return True


	def validate_meeting(self, meeting_name, meeting_token):
		check_meeting_name = bool(search(r"^[A-Za-z0-9]+$", meeting_name))
		check_meeting_token = bool(search(r"^[A-Za-z0-9]+$", meeting_token))
		if False in {check_meeting_name, check_meeting_token} or len(meeting_token) != 12:
			return False
		else:
			return True

	# ----------------------------------- HASHING AND TOKEN GENERATION ---------------------------------------------
	hasher = PasswordHasher(time_cost=2, parallelism=2, encoding='utf-8')

	def password_hash(self, pswd):
		hashed_pswd = self.hasher.hash(pswd)
		return hashed_pswd

	def password_verify(self, hashed_pswd, input_pswd):
		return self.hasher.verify(hashed_pswd, input_pswd)

	def generate_token(self):
		token = ''.join(random.choice(string.ascii_lowercase) + random.choice(string.ascii_uppercase) + random.choice(string.digits) for i in range(4))
		return token

	

	# ----------------------------------- BRUTE FORCE PROTECTION ---------------------------------------------
	def login_brute_force_protection(self, loginTries, username):
		if loginTries == 3:
			User.objects.filter(username = username).update(penaltyExpirationDate = datetime.now() + timedelta(minutes=5))
		elif loginTries == 4:
			User.objects.filter(username = username).update(penaltyExpirationDate = datetime.now()+ timedelta(minutes=30))


	def meeting_brute_force_protection(self, meeting_name):
		token_expiration = Meeting.objects.values('tokenValidUntil').filter(meetingName = meeting_name)[0].get('tokenValidUntil')
		
		if token_expiration == None:	
			return None
		elif timezone.now() > token_expiration:
			return token_expiration


	def new_token_brute_force_protection(self, meeting_name):
		token_expiration = Meeting.objects.values('newTokenDate').filter(meetingName = meeting_name)[0].get('newTokenDate')
		if token_expiration == None or token_expiration < timezone.now():
			return None
		elif token_expiration > timezone.now():
			return token_expiration 

# ----------------------------------- MEETING ---------------------------------------------

	def check_meeting_credentials(self, request, meeting_name, meeting_token):
		try:
			Meeting.objects.values('meetingName').filter(meetingName = meeting_name, meetingToken = meeting_token)[0].get('meetingName')
			request.session['meetingName'] = meeting_name
			user_id = request.session.get('user_id')
			MeetingLog(meetingName = meeting_name, participantId = user_id, accessTime = datetime.now()).save()
		except IndexError:
			notification.generate_status_message(request, 'error', "Wrong meeting name / token! Try again.")


	def meeting_admin_access(self, request, meeting_name, meeting_token):
		try:
			Meeting.objects.values('isHost').filter(meetingAdmin = request.session.get('user_id'))[0].get('isHost')
			self.check_meeting_credentials(request, meeting_name, meeting_token)
		except IndexError:
			notification.generate_status_message(request, 'error', "Only meeting host can access this meeting!")

# ----------------------------------- LOGIN ---------------------------------------------
	
	def check_penalty(self, username):
		current_penalty = User.objects.values('penaltyExpirationDate').filter(username = username)[0].get('penaltyExpirationDate')
		if current_penalty == None or current_penalty < timezone.now():
			return None
		elif current_penalty > timezone.now():
			return current_penalty

	def login_tries(self, username):
		get_current_tries = User.objects.values('loginTries').filter(username = username)[0].get('loginTries')	
		User.objects.filter(username = username).update(loginTries = get_current_tries + 1)	

		return User.objects.values('loginTries').filter(username = username)[0].get('loginTries')