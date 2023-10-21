import time
import requests
import re


def get_code_from_nada(email: str):
    if any(['@dropjar.com' in email, '@inboxbear.com' in email, '@tafmail.com' in email]):
        url = f"https://getnada.com/api/v1/inboxes/{email}"
        response = requests.get(url).json()
        try:
            subject = response['msgs'][0]['s']
            if subject == 'Proton Verification Code':
                uid = response['msgs'][0]['uid']
                code = re.search(r'\d{4,10}', requests.get(f"https://getnada.com/api/v1/messages/html/{uid}")
                                 .text.split('\n')[2])
                code = code.group() if code else code
        except:
            return None
    return code


def get_code_by_many_tries(email, tries=5, time_to_sleep=5):
    for i in range(tries):
        print(f"Try {i+1}")
        code = get_code_from_nada(email)
        if code:
            print('Code found!')
            return code
        else:
            print('Code not found.. ')
        time.sleep(time_to_sleep)
