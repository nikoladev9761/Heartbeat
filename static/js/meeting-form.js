const meeting_name = document.getElementById('meetingName5');
const meetingToken = document.getElementById('meetingToken5');
const btn = document.getElementById('submit-btn');


meeting_name.addEventListener('keyup', e => {
	checkMeetingName();
	if (checkMeetingName() === true && checkMeetingToken() === true){
		btn.disabled = false;
	} else {
		btn.disabled = true;
	}
});

meetingToken.addEventListener('keyup', e => {
	checkMeetingToken();
	if (checkMeetingName() === true && checkMeetingToken() === true){
		btn.disabled = false;
	} else {
		btn.disabled = true;
	}
});


function checkMeetingName() {
	const nameValue = meeting_name.value.trim();
	
	if (nameValue === '') {
		setErrorFor(meeting_name, "Meeting name can't be blank");
		btn.disabled = true;
		return false;

	} else if (nameValue.length !== 12){
		setErrorFor(meeting_name, "Meeting name must be 12 characters long");
		btn.disabled = true;
		return false;

	} else if (!nameValue.match(/^[A-Za-z0-9]+$/)) {	
		setErrorFor(meeting_name, "Meeting name can't contain special characters");
		btn.disabled = true;
		return false;

	}  else {
		setSuccessFor(meeting_name);
		btn.disabled = false;
		return true;
	}
}

function checkMeetingToken() {
	const tokenValue = meetingToken.value.trim();

	if (tokenValue === '') {
		setErrorFor(meetingToken, "Meeting token can't be blank");
		btn.disabled = true;
		return false;

	} else if (!tokenValue.match(/^[A-Za-z0-9]+$/)) {	
		setErrorFor(meetingToken, "Meeting token can't contain special characters");
		btn.disabled = true;
		return false;

	} else if (tokenValue.length !== 12){
		setErrorFor(meetingToken, 'Meeting token must be 12 characters long');
		btn.disabled = true;
		return false;
		
	} else {
		setSuccessFor(meetingToken);
		btn.disabled = false;
		return true;
	}
}

function setErrorFor(input, message) {
	const formControl = input.parentElement;
	const small = formControl.querySelector('small');
	formControl.className = 'form-control error';
	small.innerText = message;
}

function setSuccessFor(input) {
	const formControl = input.parentElement;
	formControl.className = 'form-control success';
}