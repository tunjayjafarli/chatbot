        var inputBox = document.getElementById("telegram-token")
        inputBox.addEventListener("focus", function() {
            this.placeholder = '';
        });
        inputBox.addEventListener("blur", function() {
            this.placeholder = 'Enter Telegram bot token';
        });
        const setError = (element, message) =>{
            const inputControl = element.parentElement;
            const errorDisplay = inputControl.querySelector(".error");

            errorDisplay.innerText = message;
            inputControl.classList.add('error');
            inputControl.classList.remove('success')
        }
            const setSuccess = element =>{
                const inputControl = element.parentElement;
                const errorDisplay = inputControl.querySelector(".error");
                errorDisplay.innerText = '';
                inputControl.classList.add('success');
                inputControl.classList.remove('error')
            }

    function submitBtn() {

        if (inputBox && inputBox.value.length == 46)
        {
            console.log(inputBox.value);
            setSuccess(inputBox);
        }
        else if (inputBox.value == '')
        {
            setError(inputBox, "Please enter your Bot Token")
        }
        else
        {
            setError(inputBox, "Please enter a valid token")
        }
}

