from heartbeat_app.models import Meeting
from .security import SecurityRepo
from .emails import EmailRepo
from datetime import datetime, timedelta
from .notification import NotificationRepo

notification = NotificationRepo()


class MeetingRepo():

	def generate_meeting_credentials(self, request, user_id):
		meeting_name = SecurityRepo().generate_token()
		meeting_pswd = SecurityRepo().generate_token()
		meeting_token = SecurityRepo().generate_token()
		meeting_pswd = SecurityRepo().password_hash(meeting_pswd)

		Meeting(meetingName = meeting_name, meetingPswd = meeting_pswd, meetingToken = meeting_token, meetingAdmin = user_id, isHost = True).save()
		request.session['meetingName'] = meeting_name


	def join_meeting(self, request, meeting_name, meeting_token):
		meeting_validation = SecurityRepo().validate_meeting(meeting_name, meeting_token)
		token_expiration_date = SecurityRepo().meeting_brute_force_protection(meeting_name)
		
		if meeting_validation == True:
			SecurityRepo().meeting_admin_access(request, meeting_name, meeting_token)			

			if token_expiration_date == None:
				SecurityRepo().check_meeting_credentials(request, meeting_name, meeting_token)
			else:
				notification.generate_status_message(request, 'error', "Token for this meeting has expired!")

		else:
			notification.generate_status_message(request, 'error', 'Meeting name / token invalid format.')

	# -------------------------------------------------------------------------------------------------------

	def send_invitations(self, request, participants, meeting_name):
		token_penalty = SecurityRepo().new_token_brute_force_protection(meeting_name)

		if token_penalty == None:
			new_meeting_token = SecurityRepo().generate_token()
			Meeting.objects.filter(meetingName = meeting_name).update(meetingToken = new_meeting_token)
			meeting_token = Meeting.objects.values('meetingToken').filter(meetingName = meeting_name)[0].get('meetingToken')
			credentials = [meeting_name, meeting_token]
			emails = str(participants).split(", ")	
			EmailRepo().send_invitations(emails, credentials)
			notification.generate_status_message(request, 'success', 'Invitations sent successfuly.')
			
			Meeting.objects.filter(meetingName = meeting_name).update(tokenValidUntil = datetime.now() + timedelta(minutes=10))
			Meeting.objects.filter(meetingName = meeting_name).update(newTokenDate = datetime.now() + timedelta(minutes=3))
		else:
			notification.generate_status_message(request, 'error', 'Unable to send token now! Try again in 3 minutes.')