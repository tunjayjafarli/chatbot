const knowledgebaseText = document.getElementById("knowledge-base-text")

const setError = (element, message) =>{
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector(".error-message");
    const successDisplay = inputControl.querySelector(".success-message");

    errorDisplay.innerText = message;
    errorDisplay.style.display = 'block';
    successDisplay.style.display = 'none';
    inputControl.classList.add('error');
    inputControl.classList.remove('success');
};

const setSuccess = (element, message) =>{
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector(".error-message");
    const successDisplay = inputControl.querySelector(".success-message");

    errorDisplay.style.display = 'none';
    successDisplay.innerText = message;
    successDisplay.style.display = 'block';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};

function knowledge_base_submitBtn(){
    if (knowledgebaseText.value == ''){
        setError(knowledgebaseText, "Please enter your Knowledge Base to Train Your Bot")
    }
    else{
        console.log(knowledgebaseText.value);
        setSuccess(knowledgebaseText, "Success")
    }
}
