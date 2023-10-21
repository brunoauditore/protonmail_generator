from guerrillamail import GuerrillaMailSession
import time


def get_guerrilla_mail(email_name, sleeping_time=5, tries_count=5, sender=None):
    session = GuerrillaMailSession(email_address=email_name)
    content = None

    for _ in range(tries_count):
        for mail in session.get_email_list():
            if 'guerrilla' not in mail.sender:
                if sender:
                    if sender in mail.sender:
                        content = session.get_email(mail.guid).body
                else:
                    content = session.get_email(mail.guid).body
            if content:
                return content.split('<br>')[1].strip('</p>')
            else:
                time.sleep(sleeping_time)

