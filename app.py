import settings
from text_ui import get_choice
from web_generators.generator_interface import create_one
from web_generators.jetbrains_account_generator import generate_with_new_email
from settings import possible_emails, protonmails_filename, jetbrains_filename
import csv


def choose_email_for_registration():
    print("You can choose one of these emails (maildrop in priotity, "
          "in my experience maildrop is the best choice): ")

    emails = {}
    question_string = ''

    for index, email in enumerate(possible_emails, start=1):
        emails.update({index: email})
        question_string += f"{index}. {email}\n"
    print(question_string)

    choice = get_choice.get_user_choice(question_string, parse_string=True)

    return emails[int(choice)]


def save_in_csv_question(data, filename):
    print("Do you want to save in csv file? (input: y/n)")
    choice = get_choice.get_user_input()
    match choice:
        case 'y':
            with open(filename + '.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerows(data)
            print('saved')
        case 'n':
            pass


def main():
    question_string = "1. Generate protonmail emails (3-4 available per day on 1 ip)" \
                      "\n2. Generate jetbrains free accounts (3-4 available per day because it'll register using" \
                      " protonmail)" \
                      "\n3. Get free pro jetbrain license (Example: Pycharm Pro) [program must be pre-installed] " \
                      "[will work soon, now in develop])" \
                      "\n4. Exit"

    print("Please don't do anything when selenium is working!!")
    print("What are you interested in? (type a number): \n")
    print(question_string)
    choice = get_choice.get_user_choice(question_string, parse_string=True)

    match choice:
        case "1":
            proton_accounts = []
            print("How many protonmail accounts do you want to get? (3-4 available per day on 1 ip)")
            accounts_count = input(">> ")
            if get_choice.is_integer(accounts_count):
                try:
                    email_for_registration = choose_email_for_registration()
                    settings.temporary_email = email_for_registration

                    for _ in range(int(accounts_count)):
                        print("Trying to create account...")
                        protonmail_login, protonmail_password = create_one()
                        proton_accounts.append([protonmail_login + ' ', protonmail_password + ' '])
                except Exception as exc:
                    print(exc)
                finally:
                    if proton_accounts:
                        print('Your emails:')
                        for item in proton_accounts:
                            print(f'Proton login: {item[0]}Proton password: {item[1]}')
                            print()
                        save_in_csv_question(data=proton_accounts, filename=protonmails_filename)
                    else:
                        print("No accounts((")
            else:
                print("You need to input an integer!")
                return

        # case "2":
        #     jetbrains_accounts = []
        #     print("How many jetbrains accounts do you want to get? (3-4 available per day because it'll register using"
        #           " protonmail)")
        #     accounts_count = input(">> ")
        #     if get_choice.is_integer(accounts_count):
        #         try:
        #             email_for_registration = choose_email_for_registration()
        #             settings.temporary_email = email_for_registration
        #
        #             for _ in range(int(accounts_count)):
        #                 print("Trying to create account...")
        #                 protonmail, protonmail_password, jetbrains_password = generate_with_new_email()
        #                 jetbrains_accounts.append([protonmail + ' ', protonmail_password + ' ', jetbrains_password +
        #                                            ' '])
        #         except Exception as exc:
        #             print(exc)
        #         finally:
        #             if jetbrains_accounts:
        #                 print('Your accounts: ')
        #                 for item in jetbrains_accounts:
        #                     print(f'Proton login: {item[0]}Proton password: {item[1]}Jetbrains password: {item[2]}')
        #                     print()
        #                 save_in_csv_question(data=jetbrains_accounts, filename=jetbrains_filename)
        #             else:
        #                 print("No accounts((")
        #     else:
        #         print("You need to input an integer!")
        #         return
        # case "3":
        #     print("Hello! This function will work soon!")
        #     input()
        #     # will be soon))
        #     pass
        # case "4":
        #     print("Bye!")
        #     return


if __name__ == '__main__':
    main()
