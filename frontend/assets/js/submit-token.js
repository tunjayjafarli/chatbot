function submitToken() {
        var error = document.getElementById("error")
        var token = document.getElementById("token")
        if (token && token.value.length == 46)
        {
            console.log(document.getElementById("token").value);
            error.textContent = ""
        } 
        else 
        {
            error.textContent = "Please enter a valid Telegram bot token"
            error.style.color = "red"
        }
}


