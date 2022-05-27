from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registration/", views.registration, name="registration"),
	path("verification/", views.verification, name="verification"),
	path("login/", views.login, name="login"),
	path("recovery/", views.recovery, name="recovery"),
	path("new-password/", views.update_password, name="update_password"),
	path("logout/", views.logout, name="logout"),
	path("leave/", views.leave_meeting, name="leave_meeting"),
	path("user/", views.profile, name="profile"),
	path("join-host/", views.join, name="join"),
	path("host/", views.host, name="host"),	
	path("meeting/", views.meeting, name="meeting"),
	path('meeting/<str:meeting_name>/', views.meeting, name="meeting")
]                                              