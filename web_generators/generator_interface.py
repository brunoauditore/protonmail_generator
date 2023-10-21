import csv
from web_generators.generator import new_protonmail
import settings


class MyGenerator:
    def __init__(self, num_of_tries=1):
        self.__bad_tries_counter = 0
        self.max_sleeping_time = settings.max_sleeping_time
        self.min_sleeping_time = settings.min_sleeping_time
        self.sleeping_time_middle = settings.middle_sleeping_time
        self.time_part = (3, 2)
        # Кількість невдалих спроб, після досягнення стоп
        self.stop_on_bad_tries = settings.stop_on_bad_tries
        # Кількість спроб всього
        self.num_of_tries = num_of_tries
        self.data = None

    def run_generator(self):
        for i in range(self.num_of_tries):
            if self.__bad_tries_counter >= self.stop_on_bad_tries:
                print("Number of bad tries reached. Stopping...")
                return
            else:
                self.__bad_tries_counter += self.get_email()

    def get_email(self):
        try:
            self.data = new_protonmail(sleeping_time_min=self.min_sleeping_time,
                                       sleeping_time_max=self.max_sleeping_time,
                                       sleeping_time_middle=self.sleeping_time_middle,
                                       time_part=self.time_part)
            return 0
        except Exception as exc:
            print(exc)
            print("Bad try! Stopping current...")
            return 1


def create_one():
    gen = MyGenerator(num_of_tries=1)
    gen.run_generator()
    data = [gen.data['login'], gen.data['password']]
    return data
