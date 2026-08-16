DATA_FILE = "doctors.txt"    # name of the text file that stores all records

CAT_MEDICAL = "Medical and Organ Specialist"   # text label for this category, used everywhere instead of retyping it
CAT_PRIMARY = "Primary Care"                   # text label for this category
CAT_SURGICAL = "Surgical Specialist"           # text label for this category


test

def make_sure_file_exists():
    # Try to open the file to see if it is already there
    try:
        file = open(DATA_FILE, "r")   # try opening doctors.txt in read mode
        file.close()                  # close it again, we only wanted to check it exists
    except FileNotFoundError:         # this runs only if the file was not found
        new_file = open(DATA_FILE, "w")   # create the file by opening it in write mode
        new_file.close()                  # close it right away, we just needed it to exist


def read_all_records():
    # Reads every line in doctors.txt and turns it into a list of records.
    # Each record is just a list: [name, contact, specialization, category]
    make_sure_file_exists()      # make sure the file is there before we try to read it
    all_records = []             # this will hold every record we find

    file = open(DATA_FILE, "r")  # open the file in read mode
    for line in file:            # go through the file one line at a time
        line = line.strip()      # remove the newline character and extra spaces
        if line == "":           # skip this loop turn if the line is empty
            continue              # go back to the top of the loop, skipping the rest below
        parts = line.split(" | ")       # break the line into pieces using " | " as the divider
        if len(parts) == 4:              # only keep it if it has exactly 4 pieces (a valid record)
            all_records.append(parts)    # add this record to our list
    file.close()                 # close the file since we're done reading

    return all_records           # give back the full list of records


def save_all_records(records):
    # Overwrites doctors.txt with the given list of records
    file = open(DATA_FILE, "w")           # open the file in write mode (this erases old content)
    for record in records:                # go through each record in the list
        name = record[0]                  # get the name from position 0
        contact = record[1]               # get the contact number from position 1
        specialization = record[2]        # get the specialization from position 2
        category = record[3]              # get the category from position 3
        file.write(f"{name} | {contact} | {specialization} | {category}\n")  # write the record as one line
    file.close()                          # close the file so the changes are saved


def get_matching_records(specialization, category):
    # Only keep the records that match the given specialization and category
    matches = []                          # this will hold only the records that match
    all_records = read_all_records()      # load every record from the file
    for record in all_records:            # check each record one by one
        if record[2] == specialization and record[3] == category:  # compare specialization and category
            matches.append(record)        # keep this record because it matches
    return matches                        # give back only the matching records


def add_record(specialization, category):
    name = input("Doctor Name: ").strip()          # ask the user for the doctor's name
    contact = input("Contact Number: ").strip()    # ask the user for the contact number

    all_records = read_all_records()               # load all existing records
    new_record = [name, contact, specialization, category]  # build the new record as a list
    all_records.append(new_record)                 # add the new record to the list
    save_all_records(all_records)                  # save the updated list back to the file

    print(f'Record for "{name}" added under {specialization} ({category}).')  # confirm to the user
    print()                                         # print a blank line for spacing


def view_records(specialization, category):
    matches = get_matching_records(specialization, category)  # get only the records for this specialization/category

    print(f"===== {specialization} ({category}) - All Records =====")  # print a header
    if len(matches) == 0:               # check if there are no matching records
        print("No records found.")      # tell the user nothing was found
        print()                         # blank line for spacing
        return                          # stop the function here, nothing more to show

    count = 1                           # counter used to number the list starting at 1
    for record in matches:              # go through each matching record
        print(f"[{count}] {record[0]} | Contact: {record[1]}")  # print the numbered record
        count = count + 1               # increase the counter by 1 for the next record
    print()                             # blank line for spacing


def search_record(specialization, category):
    query = input("Enter doctor name to search: ").strip().lower()  # get the search text, lowercase for easy matching
    matches = get_matching_records(specialization, category)        # get the records for this specialization/category

    found_any = False                   # tracks whether we found at least one match
    print(f"===== Search Results ({specialization}) =====")    # print a header
    count = 1                           # counter for numbering results
    for record in matches:              # go through each record in this category
        doctor_name = record[0]         # get this record's name
        if query in doctor_name.lower():        # check if the search text is inside the name
            print(f"[{count}] {record[0]} | Contact: {record[1]}")  # print the matching record
            count = count + 1           # move the counter forward
            found_any = True            # remember that we found something

    if not found_any:                   # if we never found a match
        print("No matching records found.")  # tell the user
    print()                             # blank line for spacing


def update_record(specialization, category):
    query = input("Enter exact doctor name to update: ").strip().lower()  # ask which doctor to update
    all_records = read_all_records()    # load all records from the file

    for record in all_records:          # go through every record
        if record[0].lower() == query and record[2] == specialization and record[3] == category:  # find the exact match
            print(f"Current -> Name: {record[0]}, Contact: {record[1]}")  # show current info
            new_name = input(f"New Name (leave blank to keep '{record[0]}'): ").strip()      # ask for a new name
            new_contact = input(f"New Contact (leave blank to keep '{record[1]}'): ").strip()  # ask for a new contact

            if new_name != "":          # only change the name if the user typed something
                record[0] = new_name    # update the name in the record
            if new_contact != "":       # only change the contact if the user typed something
                record[1] = new_contact  # update the contact in the record

            save_all_records(all_records)  # save the updated list back to the file
            print("Record updated.")       # confirm the update
            print()                        # blank line for spacing
            return                         # stop the function, we're done

    print("No matching record found.")  # this runs only if the loop never found a match
    print()                             # blank line for spacing


def delete_record(specialization, category):
    query = input("Enter exact doctor name to delete: ").strip().lower()  # ask which doctor to delete
    all_records = read_all_records()    # load all records from the file

    record_to_delete = None             # placeholder until we find the record to remove
    for record in all_records:          # go through every record
        if record[0].lower() == query and record[2] == specialization and record[3] == category:  # check for exact match
            record_to_delete = record   # remember this record as the one to delete
            break                       # stop looking, we already found it

    if record_to_delete is None:        # check if we never found a match
        print("No matching record found.")  # tell the user
        print()                         # blank line for spacing
        return                          # stop the function here

    all_records.remove(record_to_delete)  # remove the record from the list
    save_all_records(all_records)         # save the updated list back to the file
    print("Record deleted.")              # confirm the deletion
    print()                               # blank line for spacing


# ===== USER SIDE MENUS =====

def user_read_specialization(specialization, category):
    while True:                         # keep looping until the user chooses to go back
        view_records(specialization, category)   # show all records for this specialization
        answer = input("Would You Like To Go Back [Y/N]: ").strip().lower()  # ask if they want to leave
        if answer == "y":               # check if they typed "y"
            break                       # exit the loop and end this function


def user_medical_organ_specialist():
    while True:                         # keep showing this menu until the user exits
        print("[1] Cardiologists")      # menu option 1
        print("[2] Dermatologists")     # menu option 2
        print("[3] Neurologists")       # menu option 3
        print("[4] Exit")               # menu option 4
        choice = int(input("Enter an Option: "))   # get the user's choice as a number
        if choice == 1:                             # if they picked option 1
            user_read_specialization("Cardiologists", CAT_MEDICAL)   # show cardiologist records
        elif choice == 2:                            # if they picked option 2
            user_read_specialization("Dermatologists", CAT_MEDICAL)  # show dermatologist records
        elif choice == 3:                            # if they picked option 3
            user_read_specialization("Neurologists", CAT_MEDICAL)    # show neurologist records
        elif choice == 4:                            # if they picked option 4
            break                                     # leave this menu


def user_primary_care():
    while True:                         # keep showing this menu until the user exits
        print("[1] Physicians")         # menu option 1
        print("[2] Pediatricians")      # menu option 2
        print("[3] Internists")         # menu option 3
        print("[4] Exit")               # menu option 4
        choice = int(input("Enter an Option: "))   # get the user's choice as a number
        if choice == 1:                             # if they picked option 1
            user_read_specialization("Physicians", CAT_PRIMARY)      # show physician records
        elif choice == 2:                            # if they picked option 2
            user_read_specialization("Pediatricians", CAT_PRIMARY)   # show pediatrician records
        elif choice == 3:                            # if they picked option 3
            user_read_specialization("Internists", CAT_PRIMARY)      # show internist records
        elif choice == 4:                            # if they picked option 4
            break                                     # leave this menu


def user_surgical_specialist():
    while True:                         # keep showing this menu until the user exits
        print("[1] General Surgeons")               # menu option 1
        print("[2] Orthopedic Surgeons")             # menu option 2
        print("[3] Obstetricians and Gynecologists")  # menu option 3
        print("[4] Exit")                             # menu option 4
        choice = int(input("Enter an Option: "))   # get the user's choice as a number
        if choice == 1:                             # if they picked option 1
            user_read_specialization("General Surgeons", CAT_SURGICAL)  # show general surgeon records
        elif choice == 2:                            # if they picked option 2
            user_read_specialization("Orthopedic Surgeons", CAT_SURGICAL)  # show orthopedic surgeon records
        elif choice == 3:                            # if they picked option 3
            user_read_specialization("Obstetricians and Gynecologists", CAT_SURGICAL)  # show OB-GYN records
        elif choice == 4:                            # if they picked option 4
            break                                     # leave this menu


def user_menu():
    while True:                         # keep showing this menu until the user goes back
        print("===== Welcome To J2A HOSPITAL =====")   # title header
        print("[1] Medical and Organ Specialist.")      # menu option 1
        print("[2] Primary Care.")                      # menu option 2
        print("[3] Surgical Specialist.")                # menu option 3
        print("[4] Back.")                               # menu option 4
        choice = int(input("Enter an Option: "))   # get the user's choice as a number
        if choice == 1:                             # if they picked option 1
            user_medical_organ_specialist()          # open that submenu
        elif choice == 2:                            # if they picked option 2
            user_primary_care()                      # open that submenu
        elif choice == 3:                            # if they picked option 3
            user_surgical_specialist()               # open that submenu
        elif choice == 4:                            # if they picked option 4
            break                                     # leave this menu and go back


# ===== ADMIN SIDE MENUS =====

def admin_crud(specialization, category):
    while True:                         # keep showing this menu until the admin goes back
        print(f"===== {specialization} ({category}) =====")  # header for this specialization
        print("[1] Add Record")         # menu option 1
        print("[2] View All Records")   # menu option 2
        print("[3] Search Record")      # menu option 3
        print("[4] Update Record")      # menu option 4
        print("[5] Delete Record")      # menu option 5
        print("[6] Back")               # menu option 6
        choice = int(input("Enter an Option: "))   # get the admin's choice as a number
        if choice == 1:                             # if they picked option 1
            add_record(specialization, category)     # add a new doctor
        elif choice == 2:                            # if they picked option 2
            view_records(specialization, category)    # show all doctors in this category
        elif choice == 3:                            # if they picked option 3
            search_record(specialization, category)   # search for a doctor by name
        elif choice == 4:                            # if they picked option 4
            update_record(specialization, category)   # update an existing doctor
        elif choice == 5:                            # if they picked option 5
            delete_record(specialization, category)   # delete an existing doctor
        elif choice == 6:                            # if they picked option 6
            break                                     # leave this menu
        else:                                        # if they typed a number that isn't a valid option
            print("Please Select an Option [1-6]")    # tell them to choose a valid option


def admin_medical_organ_specialist():
    while True:                         # keep showing this menu until the admin exits
        print("[1] Cardiologists")      # menu option 1
        print("[2] Dermatologists")     # menu option 2
        print("[3] Neurologists")       # menu option 3
        print("[4] Exit")               # menu option 4
        choice = int(input("Enter an Option: "))   # get the admin's choice as a number
        if choice == 1:                             # if they picked option 1
            admin_crud("Cardiologists", CAT_MEDICAL)   # manage cardiologist records
        elif choice == 2:                            # if they picked option 2
            admin_crud("Dermatologists", CAT_MEDICAL)  # manage dermatologist records
        elif choice == 3:                            # if they picked option 3
            admin_crud("Neurologists", CAT_MEDICAL)    # manage neurologist records
        elif choice == 4:                            # if they picked option 4
            break                                     # leave this menu


def admin_primary_care():
    while True:                         # keep showing this menu until the admin exits
        print("[1] Physicians")         # menu option 1
        print("[2] Pediatricians")      # menu option 2
        print("[3] Internists")         # menu option 3
        print("[4] Exit")               # menu option 4
        choice = int(input("Enter an Option: "))   # get the admin's choice as a number
        if choice == 1:                             # if they picked option 1
            admin_crud("Physicians", CAT_PRIMARY)      # manage physician records
        elif choice == 2:                            # if they picked option 2
            admin_crud("Pediatricians", CAT_PRIMARY)   # manage pediatrician records
        elif choice == 3:                            # if they picked option 3
            admin_crud("Internists", CAT_PRIMARY)      # manage internist records
        elif choice == 4:                            # if they picked option 4
            break                                     # leave this menu


def admin_surgical_specialist():
    while True:                         # keep showing this menu until the admin exits
        print("[1] General Surgeons")                # menu option 1
        print("[2] Orthopedic Surgeons")              # menu option 2
        print("[3] Obstetricians and Gynecologists")  # menu option 3
        print("[4] Exit")                              # menu option 4
        choice = int(input("Enter an Option: "))   # get the admin's choice as a number
        if choice == 1:                             # if they picked option 1
            admin_crud("General Surgeons", CAT_SURGICAL)   # manage general surgeon records
        elif choice == 2:                            # if they picked option 2
            admin_crud("Orthopedic Surgeons", CAT_SURGICAL)  # manage orthopedic surgeon records
        elif choice == 3:                            # if they picked option 3
            admin_crud("Obstetricians and Gynecologists", CAT_SURGICAL)  # manage OB-GYN records
        elif choice == 4:                            # if they picked option 4
            break                                     # leave this menu


def admin_menu():
    while True:                         # keep showing this menu until the admin goes back
        print("===== Admin User =====")                # title header
        print("[1] Medical and Organ Specialist.")      # menu option 1
        print("[2] Primary Care.")                      # menu option 2
        print("[3] Surgical Specialist.")                # menu option 3
        print("[4] Back.")                               # menu option 4
        choice = int(input("Enter an Option: "))   # get the admin's choice as a number
        if choice == 1:                             # if they picked option 1
            admin_medical_organ_specialist()          # open that submenu
        elif choice == 2:                            # if they picked option 2
            admin_primary_care()                      # open that submenu
        elif choice == 3:                            # if they picked option 3
            admin_surgical_specialist()               # open that submenu
        elif choice == 4:                            # if they picked option 4
            break                                     # leave this menu and go back


# ===== MAIN PROGRAM =====

def main():
    while True:                         # keep showing this menu until the program closes
        print("===== Welcome =====")    # title header
        print("[1] Admin")              # menu option 1
        print("[2] User")               # menu option 2
        print("[3] Close Program")      # menu option 3
        choice = int(input("Enter an Option: "))   # get the user's choice as a number
        if choice == 1:                             # if they picked option 1
            admin_menu()                             # go into the admin menu
        elif choice == 2:                            # if they picked option 2
            user_menu()                              # go into the user menu
        elif choice == 3:                            # if they picked option 3
            break                                     # exit the program


main()   # start the program by calling the main function
