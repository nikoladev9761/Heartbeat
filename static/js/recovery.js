const recoveryEmail = document.getElementById('inputEmail5');
const btn = document.getElementById('submit-btn');

recoveryEmail.addEventListener('keyup', e => {
	checkEmail();
	if (checkEmail() === true){
		btn.disabled = false;
	} else {
		btn.disabled = true;
	}
});


function checkEmail() {
	const emailValue = recoveryEmail.value.trim();
	const email_regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

	if(emailValue === '') {
		setErrorFor(recoveryEmail, 'Email cannot be blank');
		btn.disabled = true;
		return false;

	} else if (!emailValue.match(email_regex)) {
		setErrorFor(recoveryEmail, 'Email format invalid');
		btn.disabled = true;
		return false;
		
	} else {
		setSuccessFor(recoveryEmail);
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