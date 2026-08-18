file_name = ('doctors.txt') #this is the file name
def create_file(): #this ensures that the file was created
    try: #it tries to open the file if not it goes to except
        file = open(file_name, 'r') #opens and reads the file
        file.close() #closes the file
    except FileNotFoundError: #if the error name is FileNotFoundError it runs this block of code below
        new_file = open (file_name, 'w') #it creates a file named "doctors.txt"
        new_file.close() #it closes the file because we already created a file

def read_all_records(): #this function just read all the data inside doctors.txt and makes it into a list
    create_file() #ensures that the file was created before it reads the file
    all_records = [] #this stores the data inside the doctors.txt and makes it an list

    file = open(file_name, "r") #opens the file as read
    for line in file: #checks everyline in the file
        line = line.strip() #strips the leading whitelines
        parts = line.split(" | ") #when we read the lines we can see that it has a | seperating the values inside doctors.txt. when we split it, it becomes a list
        if len(parts) == 4: #if its only 4 it is a valid record
            all_records.append(parts) #it add the parts if its valid in the all_record list
    file.close() #closes the file

    return all_records #returns all the list of doctors info

def save_all_records(records): #this function just overwrites the doctors.txt with the admins given information
    file = open(file_name, "w") #opens the file as read
    for record in records: #checks every record in list [name, contact, specialization, category]
        name = record[0] #gets the name from position 0 in the list
        contact = record[1] #gets the contact from position 1 in the list
        specialization = record[2] #gets the specialization from position 2 in the list
        category = record[3] #gets the category from position 3 in the list
        file.write(f"{name} | {contact} | {specialization} | {category}\n") #writes the record in one line in the doctors.txt
    file.close() #closes the file

def get_matching_records(specialization, category): #it checks the records that match the given specialization and category
    matches = [] #this list will hold the records of every match
    all_records = read_all_records() #calls the read_all_records function as all_records
    for record in all_records: #checks every line of data in all_records
        if record[2] == specialization and record[3] == category: #if it match the specialization and category
            matches.append(record) #it will be added in match
    return matches #returns the matches list

def add_record(specialization, category): #this will ask the admin whats the name of the doctor and the doctors contact info
    name = input("Doctor Name: ").strip() #asks for the doctors name
    contact = input("Contact Number: ").strip() #asks for the doctors contact info

    all_records = read_all_records() #calls the function read_all_records and the read_all_records gives a list
    new_record = [name, contact, specialization, category] #this will create a list containing the inputted doctors name and the doctors information
    all_records.append(new_record) #it just adds the new record list into the all records list
    save_all_records(all_records) #calls the function "save_all_record" and saves the newly added record

    print(f'Record for "{name}" added under {specialization} ({category}).') #this just confirms that the user successfuly saved the record 
    print() #prints a new empty line


def view_record(specialization, category): #this function just view all the records
    while True: #this will create an infinite loop to break the loop you need to use break or return
        matches = get_matching_records(specialization, category) #calls the function "get_matching_records" to view the specific specialization and category
        print(f"===== {specialization} ({category}) - All Records =====") #this will display the heading
        if len(matches) == 0: #if there are no mathches it will print no records found
            print("No records found.") 
            print()
            return

        count = 1 #start count
        for record in matches: #checks all the matched records
            print(f"Doctors ID: [{count}] | Doctors Name: {record[0]} | Contact: {record[1]} | Specialization: {record[2]}") #prints 1 line of record at a time
            count += 1 #adds counter by 1 for the next record
        user_input = input('Would you like to go back [Y/N]: ').lower() #asks if the user wants to go back
        if user_input == 'y': #if the user inputs Y or y it breaks the infinite loop
            break
        print()   


def update_record(specialization, category):
    doctors_name = input("Enter exact doctor name to update: ").strip().lower() # ask which doctor to update
    all_records = read_all_records() # load all list of records from the file
 
    for record in all_records: # go through every record in all_records 1 by 1
        if record[0].lower() == doctors_name and record[2] == specialization and record[3] == category:  #find the exact match
            print(f"Current -> Name: {record[0]}, Contact: {record[1]}")  # show current info
            new_name = input(f"New Doctors Name (leave blank to keep '{record[0]}'): ").strip()      #asks for a doctors new name
            new_contact = input(f"New Doctors Contact (leave blank to keep '{record[1]}'): ").strip()  #asks for a new doctors contact
 
            if new_name != "": #only change the name if the user typed new doctors name
                record[0] = new_name #update the doctors name
            if new_contact != "": #only change the contact if the user typed something
                record[1] = new_contact  #update the doctors contact info in the record
 
            save_all_records(all_records) #save the updated list back to the file
            print("Record updated.") #a notification that confirms the update
            print() #blank line for spacing
            return #stops the function
 
    print("No matching record found.") #this runs only if the loop never found a match
    print()     

def delete_record(specialization, category):
    doctors_name = input("Enter exact doctor name to delete: ").strip().lower() #ask which doctor to delete
    all_records = read_all_records() #load all records from the file
 
    record_to_delete = None #placeholder until we find the record to remove
    for record in all_records: #go through every record
        if record[0].lower() == doctors_name and record[2] == specialization and record[3] == category: #check for exact match
            record_to_delete = record #remember this record as the one to delete
            break #stop looking, we already found it
 
    if record_to_delete is None: #check if we never found a match
        print("No matching record found.") #tell the user
        print() #blank line for spacing
        return #stop the function here
 
    all_records.remove(record_to_delete) #remove the record from the list
    save_all_records(all_records) #save the updated list back to the file
    print("Record deleted.") #confirm the deletion
    print() #blank line for spacing

def main_menu():
    while True:
        print('===== Welcome =====')
        print('[1] Admin')
        print('[2] User')
        print('[3] Close Program')
        user_input = int(input('Enter an Option: '))
        if user_input == 1:
            admin()
        elif user_input == 2:
            user()
        elif user_input == 3:
            break

def user():
    def user_main_menu():
        while True:
            print ('===== Welcome To J2A HOSPITAL =====')
            print ('[1] Medical and Organ Specialist.')
            print('[2] Primary Care.')
            print('[3] Surgical Specialist.')
            print('[4] Back.')
            user_input = int(input('Enter an Option: '))
            if user_input == 1:
                medical_organ_specialist()
            elif user_input == 2:
                primary_care()
            elif user_input == 3:
                surgical_specialist()
            elif user_input == 4:
                break

    def medical_organ_specialist():
        while True:
            print ('[1] Cardiologists')
            print ('[2] Dermatologists')
            print ('[3] Neurologists')
            print ('[4] Exit')
            print ('Select a doctor specialization [1-3] or [4] To Exit:')
            user_input = int(input('Enter an Option: '))
            if user_input == 1:
                view_record('Cardiologists', 'Medical and Organ Specialist')
            elif user_input == 2:
                view_record('Dermatologists','Medical and Organ Specialist')
            elif user_input == 3:
                view_record('Neurologists','Medical and Organ Specialist')
            elif user_input == 4:
                break

    def primary_care():
        while True:
            print ('[1] Physicians')
            print ('[2] Pediatricians')
            print ('[3] Internists')
            print ('[4] Exit')
            print ('Select a doctor specialization [1-3] or [4] To Exit:')
            user_input = int(input('Enter an Option: '))
            if user_input == 1:
                view_record('Physicians', 'Primary Care')
            elif user_input == 2:
                view_record('Pediatricians','Primary Care')
            elif user_input == 3:
                view_record('Internists','Primary Care')
            elif user_input == 4:
                break
    def surgical_specialist():
        while True:
            print ('[1] General Surgeons')
            print ('[2] Orthopedic Surgeons')
            print ('[3] Obstetricians and Gynecologistsogists')
            print ('[4] Exit')
            print ('Select a doctor specialization [1-3] or [4] To Exit:')
            user_input = int(input('Enter an Option: '))
            if user_input == 1:
                view_record('General Surgeons', 'Surgical Specialist')
            elif user_input == 2:
                view_record('Orthopedic Surgeons','Surgical Specialist')
            elif user_input == 3:
                view_record('Obstetricians and Gynecologist','Surgical Specialist')
            elif user_input == 4:
                break


    user_main_menu()

def admin():
    def admin_main_menu():
            while True:
                print ('===== Admin User =====')
                print ('[1] Medical and Organ Specialist.')
                print('[2] Primary Care.')
                print('[3] Surgical Specialist.')
                print('[4] Back.')
                user_input = int(input('Enter an Option: '))
                if user_input == 1:
                    medical_organ_specialist()
                elif user_input == 2:
                    primary_care()
                elif user_input == 3:
                    surgical_specialist()
                elif user_input == 4:
                    break
    def crud(specialization, category):
            while True:
                print(f'===== {specialization} ({category}) =====')
                print('[1] Add Record')
                print('[2] View All Records')
                print('[3] Update Record')
                print('[4] Delete Record')
                print('[5] Back')
                user_input = int(input('Enter an Option: '))
                if user_input == 1:
                    add_record(specialization, category)
                elif user_input == 2:
                    view_record(specialization, category)
                elif user_input == 3:
                    update_record(specialization, category)
                elif user_input == 4:
                    delete_record(specialization, category)
                elif user_input == 5:
                    break
                else:
                    print('Please Select an Option [1-5]')

    def medical_organ_specialist():
        while True:
            print('===== Medical Organ Specialist =====')
            print ('[1] Cardiologists')
            print ('[2] Dermatologists')
            print ('[3] Neurologists')
            print ('[4] Exit')
            print ('Select a doctor specialization [1-3] or [4] To Exit:')
            user_input = int(input('Enter an Option: '))

            if user_input == 1:
                crud('Cardiologists', 'Medical and Organ Specialist')
            elif user_input == 2:
                crud('Dermatologists','Medical and Organ Specialist')
            elif user_input == 3:
                crud('Neurologists','Medical and Organ Specialist')
            elif user_input == 4:
                break


    def primary_care():
        while True:
            print('===== Primary Care =====')
            print ('[1] Physicians')
            print ('[2] Pediatricians')
            print ('[3] Internists')
            print ('[4] Exit')
            print ('Select a doctor specialization [1-3] or [4] To Exit:')
            user_input = int(input('Enter an Option: '))

            if user_input == 1:
                crud('Physicians', 'Primary Care')
            elif user_input == 2:
                crud('Pediatricians','Primary Care')
            elif user_input == 3:
                crud('Internists','Primary Care')
            elif user_input == 4:
                break


    def surgical_specialist():
        while True:
            print('===== Surgical Specialist =====')
            print ('[1] General Surgeons')
            print ('[2] Orthopedic Surgeons')
            print ('[3] Obstetricians and Gynecologistsogists')
            print ('[4] Exit')
            print ('Select a doctor specialization [1-3] or [4] To Exit:')
            user_input = int(input('Enter an Option: '))
            if user_input == 1:
                crud('General Surgeons', 'Surgical Specialist')
            elif user_input == 2:
                crud('Orthopedic Surgeons','Surgical Specialist')
            elif user_input == 3:
                crud('Obstetricians and Gynecologist','Surgical Specialist')
            elif user_input == 4:
                break
    admin_main_menu()
main_menu()
