const knowledgebaseText = document.getElementById("knowledge-base-text")
const SubmitButton = document.getElementById("knowledge_base_submitBtn")

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
function knowledge_base_submitBtn() {
        if (knowledgebaseText.value == '')
        {
            setError(knowledgebaseText, "Please enter your Knowledge Base to Train Your Bot")
        }
        else{

            console.log(knowledgebaseText.value);
            setSuccess(knowledgebaseText)
        }
}
