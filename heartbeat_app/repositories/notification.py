from django.contrib import messages

class NotificationRepo():

	def generate_status_message(self, request, type, msg_text):
		if type == 'error':
			return messages.add_message(request, messages.ERROR, msg_text)
		elif type == 'info':
			return messages.add_message(request, messages.INFO, msg_text)
		elif type == 'success':
			return messages.add_message(request, messages.SUCCESS, msg_text)