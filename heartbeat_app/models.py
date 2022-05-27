from django.db import models
import uuid
from datetime import datetime

class User (models.Model):
	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	username = models.CharField(max_length = 20, unique = True)
	pswd = models.CharField(max_length = 100)
	email = models.CharField(max_length = 31)
	emailToken = models.CharField(max_length=12, unique=True, blank=True)
	emailVerified = models.BooleanField(default = False)
	loginTries = models.IntegerField(default=0)
	penaltyExpirationDate = models.DateTimeField(null = True, blank=True)
	online = models.BooleanField(default=False)

class Meeting (models.Model):
	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	meetingName = models.CharField(max_length=13, unique=True)
	meetingPswd = models.CharField(max_length = 100)
	meetingToken = models.CharField(max_length=12, null=True, unique=True)
	tokenValidUntil = models.DateTimeField(null = True, blank = True)
	newTokenDate = models.DateTimeField(null = True, blank = True)
	meetingAdmin = models.CharField(max_length=50, unique=True)
	isHost = models.BooleanField(default=False) 

class MeetingLog (models.Model):
	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	meetingName = models.CharField(max_length = 13)
	participantId = models.CharField(max_length = 50)
	accessTime = models.DateTimeField(default = datetime.now())