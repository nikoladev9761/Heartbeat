from django.contrib import admin
from heartbeat_app.models import User, Meeting, MeetingLog


class UsersDisplay(admin.ModelAdmin):
	list_display = ("id", "username", "pswd", "email", "emailToken", "emailVerified", "loginTries", "penaltyExpirationDate", "online")

class MeetingsDisplay(admin.ModelAdmin):
	list_display = ("id", "meetingName", "meetingPswd", "meetingToken", "tokenValidUntil", "newTokenDate", "meetingAdmin", "isHost")	

class MeetingLogsDisplay(admin.ModelAdmin):
	list_display = ("id", "meetingName", "participantId", "accessTime")	


admin.site.register(User, UsersDisplay)
admin.site.register(Meeting, MeetingsDisplay)
admin.site.register(MeetingLog, MeetingLogsDisplay)