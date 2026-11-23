from collections import UserDict
from functools import wraps
from datetime import date, timedelta

def verify_fields(conditions: list, error_message: str = 'Wrong format.'):
    def decorator(func):
        @wraps(func)
        def inner(cls, value):
            conditions_apply = [cond(value) for cond in conditions]
            if all(conditions_apply):
                return func(cls, value)
            else:
                print(error_message)
                return None

        return inner 
    
    return decorator

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    pass

class Phone(Field):
    @verify_fields(conditions=[lambda val: len(val) == 10, lambda val: val.isdigit()], 
                   error_message='Wrong phone format. Expected 10 digits.')
    def __new__(cls, number):
        return super().__new__(cls)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = date.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        if ((date.today() - self.value).days / 365 ) > 100:
            raise ValueError("Person cannot be more than 100 years old.")

    def __str__(self):
        return date.strftime(self.value, '%d.%m.%Y')
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


class Record:
    @verify_fields(conditions=[lambda val: len(val) > 1, lambda val: val.istitle()], 
                error_message='Wrong name format. Name should start from capital letter and contain more thatn 1 letter.')
    def __new__(cls, name):
        return super().__new__(cls)

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

    def __repr__(self):
        return f'Record(name={self.name})'

    def add_birthday(self, birthday: str):
        try:
            bd = Birthday(birthday)
            self.birthday = bd
            return 'Birthday added.'
        except ValueError as e:
            return e
            
    def add_phone(self, number):
        if number not in [p.value for p in self.phones]:
            new_record = Phone(number)
            if new_record:
                self.phones.append(new_record)
                return 'Phone added.'
            else:
                return 'Phone not added.'
        else:
              return 'Phone already exists.'
              

    def remove_phone(self, number):
        ind = [n for n, p in enumerate(self.phones) if p.value == number]
        if ind:
            self.phones.pop(ind[0])
            return 'Phone removed.'
        else:
            return 'Phone does not exist.'


    def find_phone(self, number):
        phone = [p for p in self.phones if p.value == number]
        if phone:
            return phone[0]
        else:
            return 'Phone not found.'

    def edit_phone(self, old_number, new_number):
        ind = [ind for ind, p in enumerate(self.phones) if p.value == old_number]
        if ind:
            new_phone = Phone(new_number)
            if new_phone:
                self.phones[ind[0]] = new_phone
                return 'Phone edited.'
            else:
                return 'Phone not edited.'
        else:
             return 'Phone not found.'

    def show_phones(self):
        return ', '.join([p.value for p in self.phones])

    def show_birthday(self):
        return str(self.birthday) if self.birthday else None



class AddressBook(UserDict):
    def __str__(self):
        return "\n".join([str(record) for record in self.data.values()])

    def add_record(self, record: Record):
        if record is None:
            return 'Record object is None. Please provide correct record.'
        elif self.data.get(record.name.value):
            return 'Record with this name already exists.'
        else:
             self.data[record.name.value] = record
             return 'Contact added.'

    def find(self, name: str):
        return self.data.get(name)
        
    def delete(self, name: str):
        if self.data.get(name):
            self.data.pop(name)
            return 'Record deleted.'
        else:
            return 'Record with this name does not exist. Nothing to delete.'

    def get_all_birthdays(self):
        all_birthdays = Congrats()
        for name, record in self.data.items():
            bd = record.show_birthday()
            if bd:
                all_birthdays.add_congratulation(name, bd)

        return all_birthdays

    def get_upcoming_birthdays(self) -> list[dict]:
        """
        Congratulations to users for upcoming 7 days.
        Args:
            users (list of dicts): users with birthday dates.
        Returns:
            congrats (list of dicts):  users to congratulate during the upcoming 7 days. Congratulations only on weekdays.
                            If birthday on weekend - we congratulate next weekday.
        """
        now = date.today()

        congrats = Congrats()
        for name, record in self.data.items():
            bd_obj = record.birthday
            if bd_obj:
                bd = bd_obj.value
            else:
                continue
            try:
                next_bd = date(year=now.year, month=bd.month, day=bd.day)
            except ValueError:
                next_bd = date(year=now.year, month=bd.month+1, day=1)
            if next_bd < now:
                try:
                    next_bd = date(year=now.year+1, month=bd.month, day=bd.day)
                except ValueError:
                    next_bd = date(year=now.year+1, month=bd.month+1, day=1)

            # check if birthday is happening in 7 days from now
            if (next_bd - now).days <= 7:
                # check if next birthday if on weekend -> then switch congrats to monday
                if next_bd.isoweekday() >= 6:
                    next_bd += timedelta(days=8-next_bd.isoweekday()) # + 1 if it's sunday , +2 if it's saturday -> both switching to monday
                congrats.add_congratulation(name, next_bd.strftime('%d.%m.%Y'))

        return congrats

class Congrats(UserDict):
    def __init__(self):
        self.created_at = date.today().strftime("%d.%m.%Y")
        super().__init__(self)

    def __str__(self):
        sorted_dict = dict(sorted(self.data.items(), key=lambda item: date.strptime(item[1], '%d.%m.%Y')))
        return "\n".join([f"{name}: congratulations on {birthday}" for name, birthday in sorted_dict.items()])

    def add_congratulation(self, name, birthday):
        self.data[name] = birthday

    def __repr__(self):
        return f"Congrats() object for date {self.created_at}."

