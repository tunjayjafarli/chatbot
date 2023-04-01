function tknsubmit() {
        var error = document.getElementById("error")
        if (document.getElementById("token").value.length==46)
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


