import readline

from adress_book import AddressBook
from assistant import (
    parse_input, add_contact, change_contact, show_phone, show_all,
    add_birthday, show_birthday, birthdays
)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    commands_list = ("Available commands:"
        "\n\t - add <username> <phone> "
        "\n\t - change <username> <old_phone> <new_phone>"
        "\n\t - phone <username>"
        "\n\t - all "
        "\n\t - add-birthday <ім'я> <дата народження>"
        "\n\t - show-birthday <ім'я>"
        "\n\t - birthdays "
        "\n\t - close \\ exit \\ bye \\ quit.'")

    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)
        except ValueError:
            print("Please enter a valid command.")
            print(commands_list)
            continue

        if command in ["close", "exit", "bye", "quit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))
            
        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == '__main__':
    main()
