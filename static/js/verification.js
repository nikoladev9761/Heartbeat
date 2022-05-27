const code = document.getElementById('inputCode5');
const btn = document.getElementById('submit-btn');

code.addEventListener('keyup', e => {
	checkCode();
	if (checkCode() === true){
		btn.disabled = false;
	} else {
		btn.disabled = true;
	}
});


function checkCode() {
	const codeValue = code.value.trim();
	
	if (codeValue == '') {
		setErrorFor(code, "Code can't be blank");
		btn.disabled = true;
		return false;

	} else if (codeValue.length !== 12){
		setErrorFor(code, "Code must be 12 characters long.");
		btn.disabled = true;
		return false;

	} else if (!codeValue.match(/^[A-Za-z0-9]+$/)) {	
		setErrorFor(code, "Code can't contain special characters");
		btn.disabled = true;
		return false;

	} else {
		setSuccessFor(code);
		btn.disabled = false;
		return true;
	}
}

// MESSAGES
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