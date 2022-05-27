from heartbeat.settings import SMTP_SERVER, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
import smtplib, ssl
from email.mime.text import MIMEText

class EmailRepo():

	def send_email_verification(self, email, token):
		smtp_server = SMTP_SERVER
		tls_port = EMAIL_PORT
		sender = EMAIL_HOST_USER
		password = EMAIL_HOST_PASSWORD
		recipient = email
		msg = MIMEText(f"\nHere's your token: {token}")
		msg['Subject'] = 'Heartbeat Account Verification'
		msg['From'] = sender
		msg['To'] = recipient
		context = ssl.create_default_context()

		with smtplib.SMTP(smtp_server, tls_port) as server:
			server.ehlo()	
			server.starttls(context=context)
			server.ehlo()
			server.login(sender, password)
			server.sendmail(sender, recipient, msg.as_string())
			server.close()
		
			return True


	def send_invitations(self, participants, credentials):
		smtp_server = SMTP_SERVER
		tls_port = EMAIL_PORT
		sender = EMAIL_HOST_USER
		password = EMAIL_HOST_PASSWORD
		recipient = ", ".join(participants)
		msg = MIMEText(f"\nJoin Meeting with these credentials:\nMeeting Name: {credentials[0]}\nToken: {credentials[1]}\n\nNote: this token lasts only 10 minutes. After that only meeting host can send new ones.")
		msg['Subject'] = 'Meeting Credentials'
		msg['From'] = sender
		msg['To'] = recipient
		context = ssl.create_default_context()

		with smtplib.SMTP(smtp_server, tls_port) as server:
			server.ehlo()	
			server.starttls(context=context)
			server.ehlo()
			server.login(sender, password)
			server.sendmail(sender, participants, msg.as_string())
			server.close()
		
			return True