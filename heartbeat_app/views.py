from django.shortcuts import render, redirect
from django.contrib import messages
from heartbeat_app.models import User

# --------------------------------------------------------------------------------
from .repositories.emails import EmailRepo
from .repositories.registration import RegistrationRepo
from .services.registration import RegistrationService

from .repositories.login import LoginRepo
from .services.login import LoginService

from .repositories.meeting import MeetingRepo
from .services.meeting import MeetingService

email_repo = EmailRepo()

registration_repo = RegistrationRepo()
registration_service = RegistrationService(registration_repo)

login_repo = LoginRepo()
login_service = LoginService(login_repo)

meeting_repo = MeetingRepo()
meeting_service = MeetingService(meeting_repo)

# --------------------------------------------------------------------------------
def base(request):
	return render(request, 'base.html')


def index(request):
	return render(request, 'index.html')


def registration(request):
	if request.session.get('user_id'):	
		return redirect('profile')
	else:									
		if request.method == "POST":
			username = request.POST['username']
			pswd = request.POST['usr_pswd']
			email = request.POST['email']
			registration_service.register(request, username, pswd, email)
			return redirect('verification')
		else:
			return render(request, 'registration.html')


def verification(request):
	if request.session.get('user_id'):		
		return redirect('profile')
	else:
		if request.method == "POST":
			token = request.POST['code']
			registration_service.account_verification(request, token)
			return redirect('login')

	return render(request, 'verification.html')


def login(request):
	if request.session.get('user_id'):
		return redirect('profile')
	else:	
		if request.method == "POST":
			username = request.POST['username']
			pswd = request.POST['usr_pswd']
			login_service.login(request, username, pswd)

			if request.session.get('user_id'):	
				return redirect('profile')
			else:
				return render(request, 'login.html')
		else:
			return render(request, 'login.html')


def recovery(request):
	if request.method == "POST":
		recovery_email = request.POST['recovery-email']
		
		if login_service.send_recovery_token(request, recovery_email) == True:
			return redirect('update_password')
		else:
			return render(request, 'recovery.html')
	else:
		return render(request, 'recovery.html')


def update_password(request):
	if request.method == "POST":
		token = request.POST['code']
		new_pswd = request.POST['new-pswd']
		login_service.update_pswd(request, token, new_pswd)
		return redirect('login')
	else:
		return render(request, 'newPassword.html')


def logout(request):
	User.objects.filter(id = request.session.get('user_id')).update(online = False)
	request.session.pop('user_id', None)

	return redirect('login')


def leave_meeting(request):
	request.session.pop('meetingName', None)

	return redirect('join')


def profile(request):
	if request.session.get('user_id'):		
		return render(request, 'profile.html')		
	else:		
		messages.add_message(request, messages.INFO, 'Please login to access this page!')
		return redirect('login')


def join(request):
	if request.session.get('user_id'):	
		if request.method == "POST":		
			meeting_name = request.POST['meeting_name']
			meeting_token = request.POST['meeting_token']
			meeting_service.join_meeting(request, meeting_name, meeting_token)
			
			return redirect('meeting', meeting_name = meeting_name)
		else:
			return render(request, 'join-host.html')		
	else:	
		messages.add_message(request, messages.INFO, 'Please login to access this page!')	
		return redirect('login')


def host(request):
	if request.session.get('user_id'):	
		if request.method == "POST":
			user_id = request.session.get('user_id')
			meeting_service.generate_meeting_credentials(request, user_id)
			
			return redirect('meeting', meeting_name = request.session.get('meetingName'))
		else:
			return render(request, 'join-host.html')
	else:		
		messages.add_message(request, messages.INFO, 'Please login to access this page!')
		return redirect('login')


def meeting(request, meeting_name):	
	if request.session.get('user_id') and request.session.get('meetingName'):		
		if request.method == "POST":
			meeting_name = request.session.get('meetingName')
			participants = request.POST['participants']
			meeting_service.send_invitations(request, participants, meeting_name)

			return redirect('meeting', meeting_name = meeting_name)
		else:
			return render(request, 'meeting.html', {'meeting_name': meeting_name} )
	else:		
		messages.add_message(request, messages.ERROR, "You can't access this meeting!")
		return redirect('join')