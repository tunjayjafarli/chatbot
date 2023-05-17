import os
import bardapi

from constants import GOOGLE_BARD_API_KEY

def get_response_from_bard(question):
    """Send an API request and get a response."""    
    if question:
        response = bardapi.core.Bard(timeout=10).get_answer(question)
        
        return response['content']


def main():
    print('Running bard-api.py...')

    os.environ['_BARD_API_KEY'] = GOOGLE_BARD_API_KEY

    while True:
        input_text = input('> ')
        
        response = get_response_from_bard(input_text)

        print("Answer: ", response, '\n')
        

if __name__ == '__main__':
    main()