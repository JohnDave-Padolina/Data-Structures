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

#DITO GAGAWA NG FILE HANDLING
def add_record():
    print('GAGAWIN PA LANG')
def view_record():
    print('GAGAWIN PA LANG')
def update_record():
    print('GAGAWIN PA LANG')
def delete_record():
    print('GAGAWIN PA LANG')







#DITO GAGAWA NG FILE HANDLING
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
                read_specialization('cardiologist', 'Cardiologists')
            elif user_input == 2:
                read_specialization('dermatologists','Dermatologists')
            elif user_input == 3:
                read_specialization('neurologists','Neurologists')
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
                read_specialization('cardiologist', 'Cardiologists')
            elif user_input == 2:
                read_specialization('dermatologists','Dermatologists')
            elif user_input == 3:
                read_specialization('neurologists','Neurologists')
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
                read_specialization('cardiologist', 'Cardiologists')
            elif user_input == 2:
                read_specialization('dermatologists','Dermatologists')
            elif user_input == 3:
                read_specialization('neurologists','Neurologists')
            elif user_input == 4:
                break

    def read_specialization(specialization, specialization_print):
        while True:
            print(f'===== {specialization_print} =====')
            print ('DITO IPAPAKITA YUNG MGA DOCTORS BASED DUN SA SPECIALIZATION NILA')
            print ('GAGAWA PALANG NG CSV')
            user_input = input('Would You Like To Go Back [Y/N]: ')
            low = user_input.lower()
            if low == 'y':
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
                crud('Cardiologists', 'Medical Organ Specialist')
            elif user_input == 2:
                crud('Dermatologists','Medical Organ Specialist')
            elif user_input == 3:
                crud('Neurologists','Medical Organ Specialist')
            elif user_input == 4:
                break


    def primary_care():
        while True:
            print('===== Primary Care =====')
            print ('[1] Cardiologists')
            print ('[2] Dermatologists')
            print ('[3] Neurologists')
            print ('[4] Exit')
            print ('Select a doctor specialization [1-3] or [4] To Exit:')
            user_input = int(input('Enter an Option: '))
            if user_input == 1:
                crud('Cardiologists', 'Medical Organ Specialist')
            elif user_input == 2:
                crud('Dermatologists','Medical Organ Specialist')
            elif user_input == 3:
                crud('Neurologists','Medical Organ Specialist')
            elif user_input == 4:
                break


    def surgical_specialist():
        while True:
            print('===== Surgical Specialist =====')
            print ('[1] Cardiologists')
            print ('[2] Dermatologists')
            print ('[3] Neurologists')
            print ('[4] Exit')
            print ('Select a doctor specialization [1-3] or [4] To Exit:')
            user_input = int(input('Enter an Option: '))
            if user_input == 1:
                crud('Cardiologists', 'Medical Organ Specialist')
            elif user_input == 2:
                crud('Dermatologists','Medical Organ Specialist')
            elif user_input == 3:
                crud('Neurologists','Medical Organ Specialist')
            elif user_input == 4:
                break

    admin_main_menu()
main_menu()