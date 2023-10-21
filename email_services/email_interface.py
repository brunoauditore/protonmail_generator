from email_services.getnada import get_code_by_many_tries as nada_tries
from email_services.maildrop import MailDrop
from email_services.guerrilla import get_guerrilla_mail


class MailBox:
    def __init__(self):
        self.__box_name = None
        self.__domain = None
        self.__time_to_sleep = 5
        self.__tries = 15
        self.__subject = "Proton Verification Code"
        self.__code_message = None
        self.__possible_domains = ['@guerrillamail.com', '@maildrop.cc', '@dropjar.com', '@inboxbear.com', '@tafmail.com']

    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, value):
        if value not in self.__possible_domains:
            raise ValueError('Domain not supported!')
        self.__domain = value

    @property
    def box_name(self):
        return self.__box_name

    @box_name.setter
    def box_name(self, value: str):
        if len(value) < 5:
            raise ValueError('box name is too short (must be 5 or >)')
        else:
            self.__box_name = value

    @property
    def time_to_sleep(self):
        return self.__time_to_sleep

    @time_to_sleep.setter
    def time_to_sleep(self, value):
        if value < 5:
            raise ValueError('sleeping time must be > 5')
        else:
            self.__time_to_sleep = value

    @property
    def tries(self):
        return self.tries

    @tries.setter
    def tries(self, value):
        if value < 1:
            raise ValueError('Error: Tries < 1')
        else:
            self.__tries = value

    def check_values(self):
        if self.__box_name and self.__domain:
            return True

    def get_code(self):
        if not self.check_values():
            raise ValueError('email name or domain is empty')

        if self.__domain in ['@dropjar.com', '@inboxbear.com', '@tafmail.com']:
            self.__code_message = nada_tries(email=self.__box_name+self.__domain, time_to_sleep=self.__time_to_sleep,
                              tries=self.__tries)

        elif self.__domain == '@maildrop.cc':
            mail_box = MailDrop(mailbox=self.__box_name, subject_name=self.__subject, tries_to_stop=self.__tries,
                                sleeping_time=self.__time_to_sleep)
            self.__code_message = mail_box.get_code_by_many_tries()

        elif self.__domain == '@guerrillamail.com':
            self.__code_message = get_guerrilla_mail(email_name=self.__box_name, sleeping_time=
                self.__time_to_sleep, tries_count=self.__tries)

        return self.__code_message


# box = MailBox()
# box.box_name = 'eknwefwifwiefwef'
# box.domain = '@guerrillamail.com'
# print(box.box_name)
# print(box.domain)
