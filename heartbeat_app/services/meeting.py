class MeetingService():
	def __init__(self, meeting_repository):
		self._repo = meeting_repository

	def generate_meeting_credentials(self, request, user_id) -> str:
		self._repo.generate_meeting_credentials(request, user_id)

	def send_invitations(self, request, participants, meeting_name):
		self._repo.send_invitations(request, participants, meeting_name)

	def join_meeting(self, request, meeting_name, meeting_token):
		self._repo.join_meeting(request, meeting_name, meeting_token)