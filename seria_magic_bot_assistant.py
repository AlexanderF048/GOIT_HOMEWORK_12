import re
from collections import UserDict
from datetime import datetime, timedelta 
import json
from unicodedata import name



class Field:    
    def __init__(self, value):
        self.value = None # Только создаем (инициализируем) значения
        self.value=value # на этом этапе мы обращаемся и тут активируются сеттеры-геттеры
        #print("field created") 

        @property # Превращение метода в поле 
        def value(self):
            return self.value 
        @value.setter #Валидация VALUE и запись в поле
        def value(self, value):
            if isinstance(value, list):
                flag=None
                for check in value:
                    if re.search('[\+0-9]+', check):
                        flag=True
                    else:
                        flag=False
                if flag == True:
                    self.value = value
                    return self.value
            elif isinstance(value, str):
                if re.search('[a-z]+\s{1}?[a-z]+?\s{1}?[a-z]+?', value)==True or re.search('\d{2}\.\d{2}\.\d{4}', value)==True or re.search('[\+0-9]+', value)==True:
                    self.value = value
                    return self.value
            else:
                raise Exception("oooops!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")    

    def __str__(self):
        return f"{self.value}" 
    def __repr__(self):
        return f"{self}" 


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self,N=2):
        oper_list=[]
        start=N-N
        stop=N

        for val in self.data.values():            
            oper_list.append(val)
        
        while True:
            #print(start)
            #print(stop)
           

            yield oper_list[start:stop]

            start,stop=start+N,stop+N

    
class Name(Field):
    pass
    
class Phone(Field):
    pass
    
class Birthday(Field):
    pass

class Record(Field):
    def __init__(self, name, phone=None, date=None):
        self.name = Name(name)
        self.phones = []
        self.b_date = None
        self.b_day = None


    def __str__(self):
        return f'Name: {self.name}\n Phones: {self.phones}\nBirthday: {self.b_date}'

    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.add_phone(new_phone)
                self.phones.remove(phone)
                return True

    def delete_phone(self, new_phone):
        for phone in self.phones:
            if phone.value == new_phone:
                self.phones.remove(phone)
                return True

    def add_date(self, date):
        self.b_date=Birthday(date)

    def change_b_date(self, date):
        self.b_date = date

    def days_to_birthday(self):
        _today= datetime.now()
       # print(_today.date())
        b_day= datetime.strptime(self.b_date, '%d.%m.%Y')
        #print(b_day)
        zero_date=b_day.replace(year=_today.isocalendar()[0])
       # print(zero_date)
        
        
        left=zero_date-_today
        left_days=left.days+1
        
        if left_days > 0:
            print (left_days)
            self.b_day =left_days
            return self.b_day##########################
        
        elif left_days == 0:
            print("Time to spend money.")
            print (left_days)
            self.b_day =left_days 
            return self.b_day##########################
        
        elif left_days < 0:
        
            next_year=zero_date.replace(year=zero_date.year+1)
            print(next_year)
        
            left=next_year-_today
            left_days=left.days+1
            print (left_days)
            self.b_day =left_days
            return self.b_day##########################


ADDRESSBOOK = AddressBook()
file_name="contacts.json"
downloaded_book="No any downloaded books in operational memory"


def input_error(func): #decorator
    
    def wrapper(*args, **kwargs):
        try:
            result=func(*args, **kwargs)
        
        except (KeyError, ValueError, IndexError) as e:
            print(f"Input data caused the error: {e}.")
            result="----Not result.----"
        return result
    return wrapper

    
#@input_error
#--------------------------------------------------------
@input_error
def hello_handler():
    print("How can i help you?")
#--------------------------------------------------------
#@input_error
def exit_handler():
    print("Good bye!")
    exit()
#--------------------------------------------------------
#@input_error
def show_contacts_handler():

    N=int(input("Please insert number of contacts, you want, to be printed:::"))
    

    loop=ADDRESSBOOK.iterator(N)

   
    for i in next(loop):
 
        print(i)

    while True:
        if input("Press > to continue:") == ">" :

            next(loop)

        else:
            break
  
#--------------------------------------------------------
#@input_error
def add_contact_handler(name,phone,b_date):
    cl_add_record= Record(name)
    cl_add_record.add_phone(phone)
    cl_add_record.add_date(b_date)
    

    ADDRESSBOOK.add_record(cl_add_record)
    #print(ADDRESSBOOK)
    #CONTACTS[" ".join(name)]="".join(phone)
    print(f"Contact added {name} {phone} {b_date}")
#--------------------------------------------------------
#@input_error
def set_birthday(name):
    
    birthday = input("Input birthday please, FORMAT DD.MM.YYYY :")

    record_change = ADDRESSBOOK.data[name]
    record_change.change_b_date(birthday) 
    print("Changed.")
#--------------------------------------------------------
#@input_error
def change_handler(name,phone):
    
    new_phone = input("input new phone please:")

    record_change = ADDRESSBOOK.data[name]
    record_change.change_phone(old_phone=phone, new_phone=new_phone) 
    print("Changed.")
#--------------------------------------------------------
#@input_error
def phone_handler(name):
    if name in ADDRESSBOOK.data:
        print(ADDRESSBOOK.data[name])
    else:
        print("This person not defined in your contacts.")  

def delete_handler(name,phone):
    
    record_delete = ADDRESSBOOK.data[name]

    if record_delete.delete_phone(phone) is True:
        print("Deleated")

    else:
        return 'The phone number not exist'
#@input_error
#--------------------------------------------------------
def save_handler(book=ADDRESSBOOK):
    file_name="contacts.json"
    
    inner_val=[]
    json_dict_pattern={"address_book":inner_val} 
   
    for val_name, all_fields in book.data.items():         


        contact_data={val_name:[{"Name":str(all_fields.name)},{"Phones":str(all_fields.phones)},{"Birthday":str(all_fields.b_date)}]}
        inner_val.append(contact_data)
    with open(file_name, "w") as fh:
         json.dump(json_dict_pattern, fh)
         print("Saved on your HardDrive. Current directory.")
#@input_error
#--------------------------------------------------------
def download_handler():
    file_name="contacts.json"
    global downloaded_book 
    with open(file_name, "r") as fh:
        downloaded_book = json.load(fh)
        print("Downloaded from your HardDrive. Current directory.")
        
    return downloaded_book
#@input_error
#--------------------------------------------------------
def find_matches():
    global downloaded_book
    matches_were_found=[]
    if type(downloaded_book)  != dict:
    
        print("No any downloaded books in operational memory")
    else:

        find_it=input("What do you want to find in downloaded book:::")

        address_book=downloaded_book["address_book"]

        for contact in address_book:
            for person, fields in contact.items():
                #print(person)
                #print(fields)
                for field in fields:
                    #print (field)
                    for data_type, private_data in field.items():
                        #print(data_type)
                        #print (private_data)
                        if private_data.find(find_it) > -1:
                            matches_were_found.append(person)                          
    print(matches_were_found)                  

#-------------------------------------------------------- нужно указать после всех используемых функций

COMMANDS={

    "hello":hello_handler, 
    "add":add_contact_handler,
    "change":change_handler,
    "phone":phone_handler,
    "deleat phone":delete_handler,
    "show all":show_contacts_handler,
    "good bye":exit_handler,
    "close":exit_handler,
    "exit":exit_handler,
    ".":exit_handler,
    "set birthday":set_birthday,
    "save":save_handler,
    "download":download_handler,
    "matches":find_matches

    }
#--------------------------------------------------------
def command_parser(input_data):

    input_data=str(input_data.lower()) #register non-sensative

    name=[]
   
    phone=[]

    date=[]
        
    for key, value in COMMANDS.items():
        
        if input_data.startswith(key):

            if key in ["add", "change", "phone", "deleat phone", "set birthday"]:

                particles_input_data= (input_data.removeprefix(key)).strip()
                particles_input_data=particles_input_data.split(" ")
                #print(particles_input_data)
                
                for i in  particles_input_data:

                    if re.search('[a-z]+', i):
                        name.append(i)

                    elif re.search('\d{2}\.\d{2}\.\d{4}', i):
                        date.append(i)
                        
                    elif re.search('[\+0-9]+', i):
                        phone.append(i)
                    
                    
     
                command=COMMANDS[key]  
                #phone="".join(phone)
                name=" ".join(name)
                b_date="".join(date)
                #print (f'name: {name}')
                #print (f'phone: {phone}')
                #print (f'b date: {b_date}')
                out_func=command(name, phone, b_date)# Тут все еще передаются списки из компонентов составного имени и ряда телефонов введенных ранее одной строкой
                
            elif key not in ["add", "change", "phone", "deleat phone", "set birthday"]:
                   
                command=COMMANDS[key]
                out_func=command()

            return out_func

    if "out_func" not in locals(): #Проверяем находится ли доступная команда в инпут через конечный результат функции
        print("Command not definded ")
#--------------------------------------------------------
#--------------------------------------------------------
#--------------------------------------------------------
def main():
    

    while True:

        input_variable= input("Please, input your command:")

        command_parser(input_variable)
     

if __name__ == '__main__':  
    exit(main())