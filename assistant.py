from functools import wraps
from adress_book import AddressBook, Record

# decorator
def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Provide a name please."
        except KeyError:
            return "This contact does not exist."

    return inner

# functions
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    if record:
        return record.add_phone(phone)   
    else:
        record = Record(name)
        if record:
            record.add_phone(phone)
            return book.add_record(record)
        else:
            return 'Could not add contact.'

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book[name]
    return record.edit_phone(old_phone, new_phone)

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    if len(args) > 1:
        return "Returning only 1 contact per comand."
    record = book[name]
    return record.show_phones()

@input_error
def show_all(book: AddressBook):
    if not book:
        return "Contact book is empty."
    else:
        return book

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book[name]
    return record.add_birthday(birthday)

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    if len(args) > 1:
        return "Returning only 1 contact per comand."
    record = book[name]
    bd = record.show_birthday()
    if not bd:
        return 'Birthday was not added for this contact.' 
    else:
        return bd

@input_error
def birthdays(book: AddressBook):
    if not book:
        return "Contact book is empty."
    elif book.get_all_birthdays():
        congrats = book.get_upcoming_birthdays()
        if not congrats:
            return "No birthdays in upcoming 7 days."
    else:
        return "No birthdays in the Adress Book."
