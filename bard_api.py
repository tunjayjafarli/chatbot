from bardapi import Bard

from constants import GOOGLE_BARD_API_KEY

def get_response_from_bard(question):
    """
    Send an API request and get a response.
    """
    if question:
        bard = Bard(token=GOOGLE_BARD_API_KEY)

        response = bard.get_answer(question)

        return response['content']


def main():
    print('Running bard_api.py...')

    while True:
        input_text = input('> ')
        
        response = get_response_from_bard(input_text)

        print("Answer: ", response, '\n')
        

if __name__ == '__main__':
    main()