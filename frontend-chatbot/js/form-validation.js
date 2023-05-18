        const token = document.getElementById("telegram-token")

        token.addEventListener("focus", function() {
            this.placeholder = '';
        });
        token.addEventListener("blur", function() {
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

        const tokenValue = token.value.trim()

        if (tokenValue.length == 46)
        {
            console.log(token.value);
            setSuccess(token);
        }
        else if (token.value == '')
        {
            setError(token, "Please enter your Bot Token")
        }
        else
        {
            setError(token, "Please enter a valid token")
        }
}

