import os
from datetime import datetime, timedelta
print(os.getcwd())
DOCTORS_FILE = 'doctors.txt'
PATIENTS_FILE = 'patients.txt'
ILLNESS_FILE = 'illnesses.txt'
HOSPITAL_FILE = 'hospitals.txt'
CLINIC_FILE = 'clinics.txt'
CONSULT_FILE = 'consultations.txt'
SYMPTOMS_FILE = 'symptoms.txt'
MEDICAL_ACTION_FILE = 'medical_actions.txt'

SEVERITY_LEVELS = ['Mild', 'Moderate', 'Severe']
PRIORITY_LEVELS = ['Low', 'Medium', 'High']
CARE_TYPES = ['Hospital', 'Barangay Health Center']
FOLLOWUP_STATUSES = ['Required', 'Not Required', 'Completed']
WELLNESS_STATUSES = ['Improving', 'Stable', 'Critical', 'Recovered']
CONSULTATION_FIELD_COUNT = 17

# Severity automatically decides the priority level.
SEVERITY_TO_PRIORITY = {'Mild': 'Low', 'Moderate': 'Medium', 'Severe': 'High'}
# Lower number = consulted first.
PRIORITY_RANK = {'High': 0, 'Medium': 1, 'Low': 2}


def create_file(filename):
    try:
        open(filename, 'a').close()
    except:
        print("Error creating file.")


def read_records(filename, num_fields):
    records = []

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()

                if line == '':
                    continue

                data = line.split(' | ')

                if len(data) == num_fields:
                    records.append(data)

    except FileNotFoundError:
        create_file(filename)

    return records


def read_raw_records(filename):
    records = []

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.rstrip('\r\n')
                if line:
                    records.append(line.split(' | '))
    except FileNotFoundError:
        create_file(filename)

    return records


def next_file_id(records, prefix, field_index):
    existing_ids = {
        record[field_index]
        for record in records
        if len(record) > field_index and record[field_index].startswith(prefix)
    }
    number = 1
    while f"{prefix}{number:03d}" in existing_ids:
        number += 1
    return f"{prefix}{number:03d}"


def read_hospitals():
    hospitals = []
    for index, record in enumerate(read_raw_records(HOSPITAL_FILE), start=1):
        if len(record) == 3:
            record.append(f"H{index:03d}")
        if len(record) == 4:
            hospitals.append(record)
    return hospitals


def read_clinics():
    clinics = []
    hospitals = read_hospitals()
    hospital_ids = {
        hospital[0].casefold(): hospital[3]
        for hospital in hospitals
    }
    for index, record in enumerate(read_raw_records(CLINIC_FILE), start=1):
        if len(record) == 3:
            record.append(f"C{index:03d}")
        if len(record) == 4:
            record[1] = hospital_ids.get(record[1].casefold(), record[1])
            clinics.append(record)
    return clinics


def read_doctors():
    doctors = []
    hospitals = read_hospitals()
    clinics = read_clinics()
    for record in read_raw_records(DOCTORS_FILE):
        if len(record) == 4:
            specialization = record[2]
            clinic = next(
                (item for item in clinics if item[2].casefold() == specialization.casefold()),
                None
            )
            same_specialty_count = sum(
                doctor[2].casefold() == specialization.casefold()
                for doctor in doctors
            )
            slot = "09:00" if same_specialty_count % 2 == 0 else "18:00"
            if clinic:
                record.extend(["Clinic", clinic[3], slot])
            elif hospitals:
                record.extend(["Hospital", hospitals[0][3], slot])
            else:
                continue
        elif len(record) == 7 and record[4] not in ("Hospital", "Clinic"):
            # Convert the previous two-location format to one establishment.
            legacy_hospital_id, legacy_clinic_id, slot = record[4:]
            if slot == "09:00" and any(
                clinic[3] == legacy_clinic_id for clinic in clinics
            ):
                record[4:7] = ["Clinic", legacy_clinic_id, slot]
            elif any(hospital[3] == legacy_hospital_id for hospital in hospitals):
                record[4:7] = ["Hospital", legacy_hospital_id, slot]
            else:
                continue
        if len(record) == 7:
            doctors.append(record)

    return doctors


def get_doctor_establishment(doctor):
    if doctor[4] == "Hospital":
        establishment = next(
            (item for item in read_hospitals() if item[3] == doctor[5]),
            None
        )
    elif doctor[4] == "Clinic":
        establishment = next(
            (item for item in read_clinics() if item[3] == doctor[5]),
            None
        )
    else:
        establishment = None
    return doctor[4], establishment


def save_records(filename, records):
    with open(filename, 'w') as file:
        for record in records:
            file.write(' | '.join(record) + '\n')


def read_consultation_records():
    records = []
    doctors = read_doctors()

    try:
        with open(CONSULT_FILE, 'r') as file:
            for line in file:
                data = line.rstrip('\r\n').split(' | ')

                if len(data) == CONSULTATION_FIELD_COUNT:
                    records.append(data)
                elif len(data) == 12:
                    doctor_specialization = next(
                        (doctor[2] for doctor in doctors if doctor[1] == data[3]),
                        'Unspecified'
                    )
                    records.append(data + [
                        doctor_specialization,
                        'Not recorded',
                        data[6],
                        'Completed',
                        data[11]
                    ])
    except FileNotFoundError:
        create_file(CONSULT_FILE)

    return records


def save_consultation_records(records):
    save_records(CONSULT_FILE, records)


def get_record_text(prompt, required=True):
    while True:
        value = input(prompt).strip()

        if not required and value == '':
            return ''
        if required and value == '':
            print("This field cannot be empty.")
        elif '|' in value or '\n' in value or '\r' in value:
            print("The character '|' is not allowed.")
        else:
            return value


def get_appointment_datetime(time_slot="09:00"):
    appointment_day = datetime.now().date() + timedelta(days=7)
    hour, minute = (int(part) for part in time_slot.split(':'))
    return datetime.combine(
        appointment_day,
        datetime.min.time().replace(hour=hour, minute=minute)
    ).strftime(
        '%Y-%m-%d %H:%M'
    )


def get_consultation_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def get_symptom_catalog():
    symptoms = read_records(SYMPTOMS_FILE, 3)
    if not symptoms:
        print("No symptom categories found in", SYMPTOMS_FILE)
    return symptoms


def tx_select_symptom(allow_keep=False):
    symptoms = get_symptom_catalog()
    if not symptoms:
        return None

    print()
    print("===== SYMPTOM CATALOG =====")
    for index, (symptom, illness, specialization) in enumerate(symptoms, start=1):
        print(
            f"[{index}] {symptom} | Possible illness: {illness} | "
            f"Recommended specialty: {specialization}"
        )

    options = list(range(1, len(symptoms) + 1))
    if allow_keep:
        print("[0] Keep current symptoms")
        options.append(0)

    choice = get_valid_menu_choice("Select the closest matching symptom: ", options)
    if choice == 0:
        return None

    symptom, illness, specialization = symptoms[choice - 1]
    return {
        "symptom": symptom,
        "illness": illness,
        "specialization": specialization
    }


def get_valid_age():
    while True:
        age = input("Enter Age: ").strip()

        if age.isdigit():
            age = int(age)

            if 1 <= age <= 120:
                return age

        print("Invalid age. Please enter a number from 1-120.")


def get_valid_menu_choice(prompt, valid_options):
    while True:
        choice = input(prompt).strip()

        if choice.isdigit() and int(choice) in valid_options:
            return int(choice)

        print("Invalid option. Please try again.")


def get_validated_choice(prompt, allowed_values):
    while True:
        print(f"===== {prompt} =====")

        for count, allowed in enumerate(allowed_values, start=1):
            print(f"[{count}] {allowed}")

        choice = input("Enter an Option: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(allowed_values):
            return allowed_values[int(choice) - 1]

        print(f"Invalid input. Please choose a number from 1-{len(allowed_values)}.")


def search_patient(prompt_to_add=False, display_result=True):
    patients = read_records(PATIENTS_FILE, 5)

    if display_result:
        print()
        print("===== SEARCH PATIENT =====")

    patient_id = get_record_text("Enter Patient ID: ")

    for patient in patients:
        if patient[0] == patient_id:
            if display_result:
                print()
                print("Patient Found")
                print("ID:", patient[0])
                print("Name:", patient[1])
                print("Age:", patient[2])
                print("Address:", patient[3])
                print("Contact:", patient[4])
                print()
            return patient

    if prompt_to_add:
        print("Patient ID not found.")
        choice = get_valid_menu_choice(
            "Would you like to add this patient? [1] Yes [2] No: ",
            [1, 2]
        )
        if choice == 1:
            return add_patient(patient_id)
    elif display_result:
        print("Patient not found.")

    print()
    return None


def add_patient(patient_id=None):
    patients = read_records(PATIENTS_FILE, 5)

    print()
    print("===== ADD PATIENT =====")

    if patient_id is None:
        while True:
            patient_id = get_record_text("Enter Patient ID: ")
            if any(patient[0].casefold() == patient_id.casefold() for patient in patients):
                print("A patient with this ID already exists.")
            else:
                break
    elif any(patient[0].casefold() == patient_id.casefold() for patient in patients):
        print("A patient with this ID already exists.")
        return None

    name = get_record_text("Enter Patient Name: ")
    age = get_valid_age()
    address = get_record_text("Enter Address: ")
    contact = get_record_text("Enter Contact Number: ")

    patient = [patient_id, name, str(age), address, contact]

    patients.append(patient)
    save_records(PATIENTS_FILE, patients)

    print("Patient added successfully.")
    print()
    return patient


def view_patients():
    patients = read_records(PATIENTS_FILE, 5)

    print()
    print("===== PATIENT LIST =====")

    if not patients:
        print("No patient records found.")
        print()
        return

    for count, patient in enumerate(patients, start=1):
        print(f"[{count}] Patient ID: {patient[0]} | Patient Name: {patient[1]} | Age: {patient[2]} | Address: {patient[3]} | Contact Number: {patient[4]}")

    print()


def update_patient():
    patients = read_records(PATIENTS_FILE, 5)

    print()
    print("===== UPDATE PATIENT =====")

    if not patients:
        print("No patient records found.")
        print()
        return

    for count, patient in enumerate(patients, start=1):
        print(f"[{count}] Patient ID: {patient[0]} | Patient Name: {patient[1]} | Age: {patient[2]} | Address: {patient[3]} | Contact Number: {patient[4]}")

    print()

    choice = get_valid_menu_choice("Enter the Index of the record to update: ", list(range(1, len(patients) + 1)))

    patient = patients[choice - 1]

    print()
    print("Current Record")
    print(f"Patient ID: {patient[0]} | Patient Name: {patient[1]} | Age: {patient[2]} | Address: {patient[3]} | Contact Number: {patient[4]}")
    print()

    new_name = input(f"New Patient Name (leave blank to keep '{patient[1]}'): ").strip()

    new_age = input(f"New Age (leave blank to keep '{patient[2]}'): ").strip()

    while new_age != '' and not (new_age.isdigit() and 1 <= int(new_age) <= 120):
        print("Invalid age. Please enter a number from 1-120, or leave it blank.")
        new_age = input("New Age: ").strip()

    new_address = input(f"New Address (leave blank to keep '{patient[3]}'): ").strip()
    new_contact = input(f"New Contact Number (leave blank to keep '{patient[4]}'): ").strip()

    if new_name != '':
        patient[1] = new_name
    if new_age != '':
        patient[2] = new_age
    if new_address != '':
        patient[3] = new_address
    if new_contact != '':
        patient[4] = new_contact

    save_records(PATIENTS_FILE, patients)

    print()
    print("Record updated successfully.")
    print()


def delete_patient():
    patients = read_records(PATIENTS_FILE, 5)

    print()
    print("===== DELETE PATIENT =====")

    if not patients:
        print("No patient records found.")
        print()
        return

    for count, patient in enumerate(patients, start=1):
        print(f"[{count}] Patient ID: {patient[0]} | Patient Name: {patient[1]} | Age: {patient[2]} | Address: {patient[3]} | Contact Number: {patient[4]}")

    print()

    choice = get_valid_menu_choice("Enter the Index of the record to delete: ", list(range(1, len(patients) + 1)))

    patient_to_delete = patients[choice - 1]

    print()
    print("Record to Delete")
    print(f"Patient ID: {patient_to_delete[0]} | Patient Name: {patient_to_delete[1]} | Age: {patient_to_delete[2]} | Address: {patient_to_delete[3]} | Contact Number: {patient_to_delete[4]}")
    print()

    patients.remove(patient_to_delete)
    save_records(PATIENTS_FILE, patients)

    print("Record deleted successfully.")
    print()


def patient_crud():
    while True:
        print('===== Patients File Maintenance =====')
        print('[1] Add Record')
        print('[2] View All Records')
        print('[3] Update Record')
        print('[4] Delete Record')
        print('[5] Back')

        choice = get_valid_menu_choice('Enter an Option [1-5]: ', [1, 2, 3, 4, 5])

        if choice == 1:
            add_patient()
        elif choice == 2:
            view_patients()
        elif choice == 3:
            update_patient()
        elif choice == 4:
            delete_patient()
        elif choice == 5:
            break

        print()


def add_doctor():
    doctors = read_doctors()

    print()
    print("===== ADD DOCTOR =====")

    while True:
        doctor_id = get_record_text("Enter Doctor ID: ")
        if any(doctor[0].casefold() == doctor_id.casefold() for doctor in doctors):
            print("A doctor with this ID already exists.")
        else:
            break

    name = get_record_text("Enter Doctor Name: ")
    specialization = get_record_text("Enter Specialization: ")
    contact = get_record_text("Enter Contact Number: ")

    establishment_type = get_validated_choice(
        "Doctor's Single Establishment",
        ["Hospital", "Clinic"]
    )
    establishments = (
        read_hospitals()
        if establishment_type == "Hospital"
        else [
            clinic for clinic in read_clinics()
            if clinic[2].casefold() == specialization.casefold()
        ]
    )
    if not establishments:
        print(f"No {establishment_type.lower()} is available for this doctor.")
        print()
        return

    print(f"===== ASSIGN DOCTOR'S {establishment_type.upper()} =====")
    for count, establishment in enumerate(establishments, start=1):
        print(
            f"[{count}] {establishment[3]} - {establishment[0]}"
        )
    establishment_choice = get_valid_menu_choice(
        f"Select the {establishment_type.lower()}: ",
        list(range(1, len(establishments) + 1))
    )
    establishment = establishments[establishment_choice - 1]

    same_specialty_count = sum(
        doctor[2].casefold() == specialization.casefold()
        for doctor in doctors
    )
    shift = "09:00" if same_specialty_count % 2 == 0 else "18:00"
    doctor = [
        doctor_id,
        name,
        specialization,
        contact,
        establishment_type,
        establishment[3],
        shift
    ]

    doctors.append(doctor)
    save_records(DOCTORS_FILE, doctors)

    print("Doctor added successfully to", DOCTORS_FILE)
    print()


def view_doctors():
    doctors = read_doctors()

    print()
    print("===== DOCTOR LIST =====")

    if not doctors:
        print("No doctor records found.")
        print()
        return

    for count, doctor in enumerate(doctors, start=1):
        establishment_type, establishment = get_doctor_establishment(doctor)
        print(
            f"[{count}] Doctor ID: {doctor[0]} | Doctor Name: {doctor[1]} | "
            f"Specialization: {doctor[2]} | Contact Number: {doctor[3]} | "
            f"Establishment Type: {establishment_type} | "
            f"Establishment ID: {doctor[5]} | Time Slot: {doctor[6]} | "
            f"Establishment: {establishment[0] if establishment else 'Not assigned'}"
        )

    print()


def update_doctor():
    doctors = read_doctors()

    print()
    print("===== UPDATE DOCTOR =====")

    if not doctors:
        print("No doctor records found.")
        print()
        return

    for count, doctor in enumerate(doctors, start=1):
        print(f"[{count}] Doctor ID: {doctor[0]} | Doctor Name: {doctor[1]} | Specialization: {doctor[2]} | Contact Number: {doctor[3]}")

    print()

    choice = get_valid_menu_choice("Enter the Index of the record to update: ", list(range(1, len(doctors) + 1)))

    doctor = doctors[choice - 1]

    print()
    print("Current Record")
    print(f"Doctor ID: {doctor[0]} | Doctor Name: {doctor[1]} | Specialization: {doctor[2]} | Contact Number: {doctor[3]}")
    print()

    new_name = input(f"New Doctor Name (leave blank to keep '{doctor[1]}'): ").strip()
    new_specialization = input(f"New Specialization (leave blank to keep '{doctor[2]}'): ").strip()
    new_contact = input(f"New Contact Number (leave blank to keep '{doctor[3]}'): ").strip()

    if new_name != '':
        doctor[1] = new_name
    if new_specialization != '':
        assigned_establishment = next(
            (
                item for item in (
                    read_hospitals()
                    if doctor[4] == "Hospital"
                    else read_clinics()
                )
                if item[3] == doctor[5]
            ),
            None
        )
        clinic_specialization_matches = (
            doctor[4] == "Hospital"
            or (
                assigned_establishment is not None
                and assigned_establishment[2].casefold() == new_specialization.casefold()
            )
        )
        if assigned_establishment and clinic_specialization_matches:
            doctor[2] = new_specialization
            same_specialty_count = sum(
                item is not doctor and item[2].casefold() == new_specialization.casefold()
                for item in doctors
            )
            doctor[6] = "09:00" if same_specialty_count % 2 == 0 else "18:00"
        else:
            print("The current establishment cannot serve that specialization; specialization unchanged.")
    if new_contact != '':
        doctor[3] = new_contact

    save_records(DOCTORS_FILE, doctors)

    print()
    print("Record updated successfully.")
    print()


def delete_doctor():
    doctors = read_doctors()

    print()
    print("===== DELETE DOCTOR =====")

    if not doctors:
        print("No doctor records found.")
        print()
        return

    for count, doctor in enumerate(doctors, start=1):
        print(f"[{count}] Doctor ID: {doctor[0]} | Doctor Name: {doctor[1]} | Specialization: {doctor[2]} | Contact Number: {doctor[3]}")

    print()

    choice = get_valid_menu_choice("Enter the Index of the record to delete: ", list(range(1, len(doctors) + 1)))

    doctor_to_delete = doctors[choice - 1]

    print()
    print("Record to Delete")
    print(f"Doctor ID: {doctor_to_delete[0]} | Doctor Name: {doctor_to_delete[1]} | Specialization: {doctor_to_delete[2]} | Contact Number: {doctor_to_delete[3]}")
    print()

    doctors.remove(doctor_to_delete)
    save_records(DOCTORS_FILE, doctors)

    print("Record deleted successfully.")
    print()


def doctor_crud():
    while True:
        print('===== Doctors File Maintenance =====')
        print('[1] Add Record')
        print('[2] View All Records')
        print('[3] Update Record')
        print('[4] Delete Record')
        print('[5] Back')

        choice = get_valid_menu_choice('Enter an Option [1-5]: ', [1, 2, 3, 4, 5])

        if choice == 1:
            add_doctor()
        elif choice == 2:
            view_doctors()
        elif choice == 3:
            update_doctor()
        elif choice == 4:
            delete_doctor()
        elif choice == 5:
            break

        print()


def add_hospital():
    hospitals = read_hospitals()

    print()
    print("===== ADD HOSPITAL / BARANGAY HEALTH CENTER =====")

    name = get_record_text("Enter Name: ")
    care_type = get_validated_choice("Care Type", CARE_TYPES)
    location = get_record_text("Enter Location: ")
    hospital_id = next_file_id(hospitals, "H", 3)
    hospitals.append([name, care_type, location, hospital_id])
    save_records(HOSPITAL_FILE, hospitals)

    print("Hospital / Barangay Health Center added successfully.")
    print()


def view_hospitals():
    hospitals = read_hospitals()

    print()
    print("===== HOSPITAL / BARANGAY HEALTH CENTER LIST =====")

    if not hospitals:
        print("No records found.")
        print()
        return

    for count, hospital in enumerate(hospitals, start=1):
        print(f"[{count}] Hospital ID: {hospital[3]} | Name: {hospital[0]} | Care Type: {hospital[1]} | Location: {hospital[2]}")

    print()


def update_hospital():
    hospitals = read_hospitals()

    print()
    print("===== UPDATE HOSPITAL / BARANGAY HEALTH CENTER =====")

    if not hospitals:
        print("No records found.")
        print()
        return

    for count, hospital in enumerate(hospitals, start=1):
        print(f"[{count}] Hospital ID: {hospital[3]} | Name: {hospital[0]} | Care Type: {hospital[1]} | Location: {hospital[2]}")

    print()

    choice = get_valid_menu_choice("Enter the Index of the record to update: ", list(range(1, len(hospitals) + 1)))

    hospital = hospitals[choice - 1]

    print()
    print("Current Record")
    print(f"Hospital ID: {hospital[3]} | Name: {hospital[0]} | Care Type: {hospital[1]} | Location: {hospital[2]}")
    print()

    new_name = input(f"New Name (leave blank to keep '{hospital[0]}'): ").strip()

    print(f"Current Care Type: {hospital[1]}")
    print("[0] Keep current value")

    for count, allowed in enumerate(CARE_TYPES, start=1):
        print(f"[{count}] {allowed}")

    care_choice = get_valid_menu_choice("Enter an Option: ", list(range(0, len(CARE_TYPES) + 1)))

    if new_name != '':
        hospital[0] = new_name
    if care_choice != 0:
        hospital[1] = CARE_TYPES[care_choice - 1]

    save_records(HOSPITAL_FILE, hospitals)

    print()
    print("Record updated successfully.")
    print()


def delete_hospital():
    hospitals = read_hospitals()

    print()
    print("===== DELETE HOSPITAL / BARANGAY HEALTH CENTER =====")

    if not hospitals:
        print("No records found.")
        print()
        return

    for count, hospital in enumerate(hospitals, start=1):
        print(f"[{count}] Hospital ID: {hospital[3]} | Name: {hospital[0]} | Care Type: {hospital[1]}")

    print()

    choice = get_valid_menu_choice("Enter the Index of the record to delete: ", list(range(1, len(hospitals) + 1)))

    hospital_to_delete = hospitals[choice - 1]

    print()
    print("Record to Delete")
    print(f"Hospital ID: {hospital_to_delete[3]} | Name: {hospital_to_delete[0]} | Care Type: {hospital_to_delete[1]}")
    print()

    hospitals.remove(hospital_to_delete)
    save_records(HOSPITAL_FILE, hospitals)

    print("Record deleted successfully.")
    print()


def hospital_crud():
    while True:
        print('===== Hospital / Barangay Health Center File Maintenance =====')
        print('[1] Add Record')
        print('[2] View All Records')
        print('[3] Update Record')
        print('[4] Delete Record')
        print('[5] Back')

        choice = get_valid_menu_choice('Enter an Option [1-5]: ', [1, 2, 3, 4, 5])

        if choice == 1:
            add_hospital()
        elif choice == 2:
            view_hospitals()
        elif choice == 3:
            update_hospital()
        elif choice == 4:
            delete_hospital()
        elif choice == 5:
            break

        print()


def add_clinic():
    clinics = read_clinics()

    print()
    print("===== ADD SPECIALTY CLINIC =====")

    clinic_name = get_record_text("Enter Clinic Name: ")
    hospitals = read_hospitals()
    if not hospitals:
        print("Add a hospital or health center before adding a clinic.")
        return
    for count, hospital in enumerate(hospitals, start=1):
        print(f"[{count}] {hospital[3]} - {hospital[0]}")
    hospital_choice = get_valid_menu_choice(
        "Select the linked hospital: ",
        list(range(1, len(hospitals) + 1))
    )
    hospital = hospitals[hospital_choice - 1]
    specialization = get_record_text("Enter Linked Specialization: ")
    clinic_id = next_file_id(clinics, "C", 3)
    clinics.append([clinic_name, hospital[3], specialization, clinic_id])
    save_records(CLINIC_FILE, clinics)

    print("Specialty Clinic added successfully.")
    print()


def view_clinics():
    clinics = read_clinics()

    print()
    print("===== SPECIALTY CLINIC LIST =====")

    if not clinics:
        print("No specialty clinics found.")
        print()
        return

    for count, clinic in enumerate(clinics, start=1):
        print(f"[{count}] Clinic ID: {clinic[3]} | Clinic Name: {clinic[0]} | Hospital ID: {clinic[1]} | Specialization: {clinic[2]}")

    print()


def update_clinic():
    clinics = read_clinics()

    print()
    print("===== UPDATE SPECIALTY CLINIC =====")

    if not clinics:
        print("No specialty clinics found.")
        print()
        return

    for count, clinic in enumerate(clinics, start=1):
        print(f"[{count}] Clinic ID: {clinic[3]} | Clinic Name: {clinic[0]} | Hospital ID: {clinic[1]} | Specialization: {clinic[2]}")

    print()

    choice = get_valid_menu_choice("Enter the Index of the record to update: ", list(range(1, len(clinics) + 1)))

    clinic = clinics[choice - 1]

    print()
    print("Current Record")
    print(f"Clinic ID: {clinic[3]} | Clinic Name: {clinic[0]} | Hospital ID: {clinic[1]} | Specialization: {clinic[2]}")
    print()

    new_name = input(f"New Clinic Name (leave blank to keep '{clinic[0]}'): ").strip()
    new_specialization = input(f"New Linked Specialization (leave blank to keep '{clinic[2]}'): ").strip()

    if new_name != '':
        clinic[0] = new_name
    if new_specialization != '':
        clinic[2] = new_specialization

    save_records(CLINIC_FILE, clinics)

    print()
    print("Record updated successfully.")
    print()


def delete_clinic():
    clinics = read_clinics()

    print()
    print("===== DELETE SPECIALTY CLINIC =====")

    if not clinics:
        print("No specialty clinics found.")
        print()
        return

    for count, clinic in enumerate(clinics, start=1):
        print(f"[{count}] Clinic ID: {clinic[3]} | Clinic Name: {clinic[0]} | Linked Specialization: {clinic[2]}")

    print()

    choice = get_valid_menu_choice("Enter the Index of the record to delete: ", list(range(1, len(clinics) + 1)))

    clinic_to_delete = clinics[choice - 1]

    print()
    print("Record to Delete")
    print(f"Clinic ID: {clinic_to_delete[3]} | Clinic Name: {clinic_to_delete[0]} | Linked Specialization: {clinic_to_delete[2]}")
    print()

    clinics.remove(clinic_to_delete)
    save_records(CLINIC_FILE, clinics)

    print("Record deleted successfully.")
    print()


def clinic_crud():
    while True:
        print('===== Specialty Clinic File Maintenance =====')
        print('[1] Add Record')
        print('[2] View All Records')
        print('[3] Update Record')
        print('[4] Delete Record')
        print('[5] Back')

        choice = get_valid_menu_choice('Enter an Option [1-5]: ', [1, 2, 3, 4, 5])

        if choice == 1:
            add_clinic()
        elif choice == 2:
            view_clinics()
        elif choice == 3:
            update_clinic()
        elif choice == 4:
            delete_clinic()
        elif choice == 5:
            break

        print()


def add_illness():
    illnesses = read_records(ILLNESS_FILE, 3)

    print()
    print("===== ADD ILLNESS =====")

    illness_name = input("Enter Illness Name: ").strip()

    severity = get_validated_choice("Severity", SEVERITY_LEVELS)
    priority = get_validated_choice("Priority", PRIORITY_LEVELS)

    illnesses.append([illness_name, severity, priority])
    save_records(ILLNESS_FILE, illnesses)

    print("Illness added successfully.")
    print()


def view_illnesses():
    illnesses = read_records(ILLNESS_FILE, 3)

    print()
    print("===== ILLNESS LIST =====")

    if not illnesses:
        print("No illness records found.")
        print()
        return

    for count, illness in enumerate(illnesses, start=1):
        print(f"[{count}] Illness Name: {illness[0]} | Severity: {illness[1]} | Priority: {illness[2]}")

    print()


def update_illness():
    illnesses = read_records(ILLNESS_FILE, 3)

    print()
    print("===== UPDATE ILLNESS =====")

    if not illnesses:
        print("No illness records found.")
        print()
        return

    for count, illness in enumerate(illnesses, start=1):
        print(f"[{count}] Illness Name: {illness[0]} | Severity: {illness[1]} | Priority: {illness[2]}")

    print()

    choice = get_valid_menu_choice("Enter the Index of the record to update: ", list(range(1, len(illnesses) + 1)))

    illness = illnesses[choice - 1]

    print()
    print("Current Record")
    print(f"Illness Name: {illness[0]} | Severity: {illness[1]} | Priority: {illness[2]}")
    print()

    new_name = input(f"New Illness Name (leave blank to keep '{illness[0]}'): ").strip()

    print(f"Current Severity: {illness[1]}")
    print("[0] Keep current value")

    for count, allowed in enumerate(SEVERITY_LEVELS, start=1):
        print(f"[{count}] {allowed}")

    severity_choice = get_valid_menu_choice("Enter an Option: ", list(range(0, len(SEVERITY_LEVELS) + 1)))

    print(f"Current Priority: {illness[2]}")
    print("[0] Keep current value")

    for count, allowed in enumerate(PRIORITY_LEVELS, start=1):
        print(f"[{count}] {allowed}")

    priority_choice = get_valid_menu_choice("Enter an Option: ", list(range(0, len(PRIORITY_LEVELS) + 1)))

    if new_name != '':
        illness[0] = new_name
    if severity_choice != 0:
        illness[1] = SEVERITY_LEVELS[severity_choice - 1]
    if priority_choice != 0:
        illness[2] = PRIORITY_LEVELS[priority_choice - 1]

    save_records(ILLNESS_FILE, illnesses)

    print()
    print("Record updated successfully.")
    print()


def delete_illness():
    illnesses = read_records(ILLNESS_FILE, 3)

    print()
    print("===== DELETE ILLNESS =====")

    if not illnesses:
        print("No illness records found.")
        print()
        return

    for count, illness in enumerate(illnesses, start=1):
        print(f"[{count}] Illness Name: {illness[0]} | Severity: {illness[1]} | Priority: {illness[2]}")

    print()

    choice = get_valid_menu_choice("Enter the Index of the record to delete: ", list(range(1, len(illnesses) + 1)))

    illness_to_delete = illnesses[choice - 1]

    print()
    print("Record to Delete")
    print(f"Illness Name: {illness_to_delete[0]} | Severity: {illness_to_delete[1]} | Priority: {illness_to_delete[2]}")
    print()

    illnesses.remove(illness_to_delete)
    save_records(ILLNESS_FILE, illnesses)

    print("Record deleted successfully.")
    print()


def illness_crud():
    while True:
        print('===== Illnesses Record File Maintenance =====')
        print('[1] Add Record')
        print('[2] View All Records')
        print('[3] Update Record')
        print('[4] Delete Record')
        print('[5] Back')

        choice = get_valid_menu_choice('Enter an Option [1-5]: ', [1, 2, 3, 4, 5])

        if choice == 1:
            add_illness()
        elif choice == 2:
            view_illnesses()
        elif choice == 3:
            update_illness()
        elif choice == 4:
            delete_illness()
        elif choice == 5:
            break

        print()


def view_patient_history():
    consultations = read_consultation_records()

    print()
    print("===== PATIENT CONSULTATION HISTORY =====")

    patient_id = input("Enter Patient ID: ").strip()
    print_consultation_history(patient_id, consultations)


def print_consultation_history(patient_id, consultations):
    matches = [record for record in consultations if record[1] == patient_id]

    if not matches:
        print("No consultation history found for this patient.")
        print()
        return

    print()
    print(f"Consultation History for Patient ID: {patient_id}")
    print()

    for count, record in enumerate(matches, start=1):
        print(f"===== VISIT {count} =====")
        print("Consultation ID:", record[0])
        print("Doctor:", record[3])
        print("Specialization:", record[12])
        doctor = next(
            (item for item in read_doctors() if item[1] == record[3]),
            None
        )
        if doctor:
            establishment_type, establishment = get_doctor_establishment(doctor)
            print(
                f"{establishment_type}: "
                f"{establishment[0]} ({establishment[3]})"
                if establishment else "Establishment: Not assigned"
            )
        print("Symptoms:", record[13])
        print("Doctor Findings:", record[14] or "Not recorded")
        print("Severity:", record[7])
        print("Priority:", record[8])
        print("Follow-Up:", record[9])
        print("Wellness:", record[10])
        print("Appointment Date and Time:", record[11])
        print("Appointment Status:", record[15])
        print("Consultation Date and Time:", record[16] or "Not recorded")
        print()


def file_maintenance():
    while True:
        print('===== File Maintenance =====')
        print('[1] Patients')
        print('[2] Doctors')
        print('[3] Hospital / Barangay Health Center')
        print('[4] Specialty Clinic')
        print('[5] Illnesses Record')
        print('[6] Back')

        choice = get_valid_menu_choice('Enter an Option [1-6]: ', [1, 2, 3, 4, 5, 6])

        if choice == 1:
            patient_crud()
        elif choice == 2:
            doctor_crud()
        elif choice == 3:
            hospital_crud()
        elif choice == 4:
            clinic_crud()
        elif choice == 5:
            illness_crud()
        elif choice == 6:
            break

        print()


def tx_search_patient():
    return search_patient(prompt_to_add=True, display_result=False)


def tx_view_patient_profile(patient):
    if patient is None:
        print("No patient selected.")
        print()
        return

    print()
    print("===== PATIENT PROFILE =====")
    print("Patient ID:", patient[0])
    print("Name:", patient[1])
    print("Age:", patient[2])
    print("Address:", patient[3])
    print("Contact:", patient[4])
    print()


def tx_select_doctor(recommended_specialization):
    doctors = read_doctors()
    matching_doctors = [
        doctor for doctor in doctors
        if doctor[2].strip().casefold() == recommended_specialization.strip().casefold()
    ]

    print()
    print("===== SELECT SPECIALIST =====")

    if not matching_doctors:
        print(
            f"No doctors are listed with the {recommended_specialization} "
            f"specialization. Add one in File Maintenance > Doctors."
        )
        print()
        return None

    for count, doctor in enumerate(matching_doctors, start=1):
        print(f"[{count}] {doctor[1]} - {doctor[2]}")

    choice = get_valid_menu_choice(
        "Enter an Option: ",
        list(range(1, len(matching_doctors) + 1))
    )

    selected = matching_doctors[choice - 1]

    print("Assigned Doctor:", selected[1])
    print("Specialization:", selected[2])
    establishment_type, establishment = get_doctor_establishment(selected)
    print("Assigned time:", selected[6])
    print(
        f"{establishment_type}: {establishment[0]} ({establishment[3]})"
        if establishment else "Establishment: Not assigned"
    )
    print(
        "Patient should go to:",
        f"{establishment[0]} ({establishment[3]})"
        if establishment else "Assigned establishment not available"
    )
    print()

    return selected


def tx_create_appointment():
    print()
    print("===== NEW APPOINTMENT =====")
    patient = tx_search_patient()

    if not patient:
        return

    tx_view_patient_profile(patient)
    symptom_category = tx_select_symptom()
    if not symptom_category:
        return

    print("Possible illness category:", symptom_category["illness"])
    print("Recommended specialization:", symptom_category["specialization"])
    print("This symptom match is guidance only, not a medical diagnosis.")
    doctor = tx_select_doctor(symptom_category["specialization"])

    if not doctor:
        return

    # Severity decides the priority automatically:
    # Severe -> High, Moderate -> Medium, Mild -> Low
    severity = get_validated_choice("Severity Level", SEVERITY_LEVELS)
    priority = SEVERITY_TO_PRIORITY[severity]
    print(f"Priority Level (set automatically): {priority}")

    appointment_datetime = get_appointment_datetime(doctor[6])
    consultations = read_consultation_records()
    numeric_ids = [int(record[0]) for record in consultations if record[0].isdigit()]
    consultation_id = str(max(numeric_ids, default=0) + 1)

    record = [
        consultation_id,
        patient[0],
        patient[1],
        doctor[1],
        "N/A",
        doctor[2],
        symptom_category["illness"],
        severity,
        priority,
        "",
        "",
        appointment_datetime,
        doctor[2],
        symptom_category["symptom"],
        "",
        "Scheduled",
        ""
    ]
    consultations.append(record)
    save_consultation_records(consultations)

    print("Appointment saved to", CONSULT_FILE)
    print("Appointment ID:", consultation_id)
    establishment_type, establishment = get_doctor_establishment(doctor)
    print("Assigned Doctor:", doctor[1], "-", doctor[2])
    print(
        f"{establishment_type}: {establishment[0]} ({establishment[3]})"
        if establishment else "Establishment: Not assigned"
    )
    print("Severity:", severity)
    print("Priority:", priority)
    print("Assigned time slot:", doctor[6])
    print("Appointment:", appointment_datetime)
    print()


def tx_update_consultation():
    consultations = read_consultation_records()

    print()
    print("===== CONSULTATION UPDATE =====")

    if not consultations:
        print("No appointment records are available to update.")
        print()
        return

    for count, record in enumerate(consultations, start=1):
        doctor = next(
            (item for item in read_doctors() if item[1] == record[3]),
            None
        )
        establishment_type, establishment = (
            get_doctor_establishment(doctor) if doctor else ("Establishment", None)
        )
        print(
            f"[{count}] ID: {record[0]} | Patient: {record[2]} | "
            f"Doctor: {record[3]} ({record[12]}) | "
            f"Appointment: {record[11]} | Status: {record[15]} | "
            f"{establishment_type}: "
            f"{establishment[0] if establishment else 'Not assigned'}"
        )

    choice = get_valid_menu_choice(
        "Select the appointment to update: ",
        list(range(1, len(consultations) + 1))
    )
    record = consultations[choice - 1]

    patients = read_records(PATIENTS_FILE, 5)
    patient = next((item for item in patients if item[0] == record[1]), None)
    if patient:
        tx_view_patient_profile(patient)

    print("Current symptoms:", record[13])
    symptom_category = tx_select_symptom(allow_keep=True)
    if symptom_category:
        record[13] = symptom_category["symptom"]
        record[6] = symptom_category["illness"]
        print("Possible illness category:", symptom_category["illness"])
        print("Recommended specialty:", symptom_category["specialization"])
        print("This symptom match is guidance only, not a medical diagnosis.")

    record[14] = get_record_text("Enter Doctor Findings / Diagnosis: ")
    record[16] = get_consultation_datetime()
    record[9] = get_validated_choice("Follow-up Status", FOLLOWUP_STATUSES)
    record[10] = get_validated_choice("Wellness Status", WELLNESS_STATUSES)
    record[15] = "Completed"
    save_consultation_records(consultations)

    print("Consultation updated in", CONSULT_FILE)
    print("Appointment ID:", record[0])
    print()


def transaction_menu():
    while True:
        print("===== TRANSACTIONS =====")
        print("[1] New Appointment")
        print("[2] Consultation Update")
        print("[3] Return to Main Menu")

        choice = get_valid_menu_choice("Enter an Option: ", [1, 2, 3])

        if choice == 1:
            tx_create_appointment()
        elif choice == 2:
            tx_update_consultation()
        else:
            break

        print()


def view_transactions():

    consultations = read_consultation_records()

    print()
    print("===== APPOINTMENT AND CONSULTATION RECORDS =====")

    if not consultations:
        print("No appointment or consultation records found.")
        print()
        return

    for count, record in enumerate(consultations, start=1):

        print(f"===== APPOINTMENT {count} =====")
        print("Appointment ID:", record[0])
        print("Patient ID:", record[1])
        print("Patient Name:", record[2])
        print("Doctor:", record[3])
        print("Specialization:", record[12])
        doctor = next(
            (item for item in read_doctors() if item[1] == record[3]),
            None
        )
        if doctor:
            establishment_type, establishment = get_doctor_establishment(doctor)
            print(
                f"{establishment_type}: "
                f"{establishment[0]} ({establishment[3]})"
                if establishment else "Establishment: Not assigned"
            )
        print("Possible Illness Category:", record[6] or "Not recorded")
        print("Symptoms:", record[13])
        print("Severity:", record[7] or "Not recorded")
        print("Priority:", record[8] or "Not recorded")
        print("Appointment Date and Time:", record[11])
        print("Status:", record[15])
        print("Doctor Findings / Diagnosis:", record[14] or "Not recorded")
        print("Consultation Date and Time:", record[16] or "Not recorded")
        print("Follow-Up:", record[9] or "Not recorded")
        print("Wellness:", record[10] or "Not recorded")
        print()


def system_statistics():

    patients = read_records(PATIENTS_FILE, 5)
    doctors = read_doctors()
    hospitals = read_hospitals()
    clinics = read_clinics()
    illnesses = read_records(ILLNESS_FILE, 3)
    consultations = read_consultation_records()

    print()
    print("===== SYSTEM STATISTICS =====")
    print("Total Patients:", len(patients))
    print("Total Doctors:", len(doctors))
    print("Total Hospitals / Health Centers:", len(hospitals))
    print("Total Specialty Clinics:", len(clinics))
    print("Total Illness Records:", len(illnesses))
    print("Total Appointment / Consultation Records:", len(consultations))
    print()


# ============================================================
#  QUEUE AND STACK DATA STRUCTURES
# ============================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    """Linked-list PRIORITY queue. FRONT = next patient, REAR = last patient."""

    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def is_empty(self):
        return self.front is None

    def enqueue(self, data):
        node = Node(data)
        if self.rear is None:
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node
        self.size += 1

    def enqueue_priority(self, data):
        """Sorted insert by data['sort_key']; equal keys stay first-come-first-served."""
        node = Node(data)
        if self.front is None:
            self.front = self.rear = node
        elif data["sort_key"] < self.front.data["sort_key"]:
            node.next = self.front
            self.front = node
        else:
            current = self.front
            while current.next and current.next.data["sort_key"] <= data["sort_key"]:
                current = current.next
            node.next = current.next
            current.next = node
            if node.next is None:
                self.rear = node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        node = self.front
        self.front = node.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return node.data

    def peek(self):
        return None if self.is_empty() else self.front.data

    def to_list(self):
        """Returns items from FRONT to REAR."""
        items = []
        current = self.front
        while current:
            items.append(current.data)
            current = current.next
        return items


class Stack:
    """LIFO linked-list stack. TOP = latest medical action."""

    def __init__(self):
        self.top = None
        self.size = 0

    def is_empty(self):
        return self.top is None

    def push(self, data):
        node = Node(data)
        node.next = self.top
        self.top = node
        self.size += 1

    def pop(self):
        if self.is_empty():
            return None
        node = self.top
        self.top = node.next
        self.size -= 1
        return node.data

    def peek(self):
        return None if self.is_empty() else self.top.data

    def to_list(self):
        """Returns items from TOP to BOTTOM."""
        items = []
        current = self.top
        while current:
            items.append(current.data)
            current = current.next
        return items


# ============================================================
#  SHARED STATE FOR QUEUING SYSTEM AND MEDICAL ACTION HISTORY
# ============================================================

consultation_queue = Queue()
medical_action_stack = Stack()
working_consultations = []   # in-memory copy of consultations.txt
touched_ids = set()          # consultation IDs changed but not yet saved


def sync_working_consultations():
    """Loads consultations.txt. Unsaved changes are never overwritten."""
    global working_consultations
    file_records = read_consultation_records()

    if not touched_ids:
        working_consultations = file_records
    else:
        known_ids = {record[0] for record in working_consultations}
        working_consultations.extend(
            record for record in file_records if record[0] not in known_ids
        )


def find_working_record(consultation_id):
    return next(
        (record for record in working_consultations if record[0] == consultation_id),
        None
    )


def refresh_queue():
    """Rebuilds the priority queue from Scheduled / In Consultation records."""
    global consultation_queue
    sync_working_consultations()
    new_queue = Queue()
    doctors = read_doctors()

    for record in working_consultations:
        if record[15] not in ("Scheduled", "In Consultation"):
            continue
        if record[8] not in PRIORITY_RANK:
            continue  # old records with no priority are skipped

        facility = "Not assigned"
        doctor = next((d for d in doctors if d[1] == record[3]), None)
        if doctor:
            _, establishment = get_doctor_establishment(doctor)
            if establishment:
                facility = establishment[0]

        in_consult = record[15] == "In Consultation"
        number = int(record[0]) if record[0].isdigit() else 0
        new_queue.enqueue_priority({
            "queue_number": f"Q-{number:03d}",
            "consultation_id": record[0],
            "patient_id": record[1],
            "patient_name": record[2],
            "illness": record[6] or "Not recorded",
            "doctor": record[3],
            "facility": facility,
            "severity": record[7],
            "priority": record[8],
            "status": "In Consultation" if in_consult else "Waiting",
            # in-progress patient stays first, then High > Medium > Low,
            # then earliest appointment, then lowest ID
            "sort_key": (
                0 if in_consult else 1,
                PRIORITY_RANK[record[8]],
                record[11],
                number
            )
        })

    consultation_queue = new_queue


def save_transaction_records(quiet=False):
    if not touched_ids:
        if not quiet:
            print("There are no unsaved changes.")
        return

    # Merge by ID so appointments added elsewhere are never lost.
    file_records = read_consultation_records()
    updates = {
        record[0]: record
        for record in working_consultations
        if record[0] in touched_ids
    }
    for index, record in enumerate(file_records):
        if record[0] in updates:
            file_records[index] = updates[record[0]]

    save_consultation_records(file_records)
    touched_ids.clear()
    if not quiet:
        print("Transaction records saved to", CONSULT_FILE)


def prompt_save_if_unsaved():
    if touched_ids:
        choice = get_valid_menu_choice(
            "You have unsaved changes. Save now? [1] Yes [2] No: ",
            [1, 2]
        )
        if choice == 1:
            save_transaction_records()


def save_action_history():
    """Writes the whole Medical Action History stack to medical_actions.txt.
    Lines are written from BOTTOM to TOP so the file reads oldest to newest."""
    with open(MEDICAL_ACTION_FILE, 'w') as file:
        for action in reversed(medical_action_stack.to_list()):
            # 5 info fields, then the 17 fields of the old record (used by Undo)
            line = [
                action["timestamp"],
                action["action"],
                action["consultation_id"],
                action["patient_id"],
                action["message"]
            ] + action["before"]
            file.write(' | '.join(line) + '\n')


def load_action_history():
    """Rebuilds the Medical Action History stack from medical_actions.txt."""
    try:
        with open(MEDICAL_ACTION_FILE, 'r') as file:
            for line in file:
                data = line.rstrip('\r\n').split(' | ')
                if len(data) != 5 + CONSULTATION_FIELD_COUNT:
                    continue
                before = data[5:]
                medical_action_stack.push({
                    "timestamp": data[0],
                    "action": data[1],
                    "message": data[4],
                    "consultation_id": data[2],
                    "patient_id": data[3],
                    "before": before,
                    "entry": {
                        "consultation_id": data[2],
                        "patient_id": data[3]
                    }
                })
    except FileNotFoundError:
        create_file(MEDICAL_ACTION_FILE)


def persist_changes():
    """Saves consultations.txt and medical_actions.txt right away."""
    save_transaction_records(quiet=True)
    save_action_history()
    print("Saved to", CONSULT_FILE, "and", MEDICAL_ACTION_FILE)


def push_action(action, message, record_before, queue_entry):
    medical_action_stack.push({
        "timestamp": get_consultation_datetime(),
        "action": action,
        "message": message,
        "consultation_id": queue_entry["consultation_id"],
        "patient_id": queue_entry["patient_id"],
        "before": record_before,
        "entry": queue_entry
    })
    persist_changes()


def display_queue(title="PATIENT CONSULTATION QUEUE"):
    print()
    print(title)

    if consultation_queue.is_empty():
        print("No patient is currently waiting.")
        return

    print("FRONT")
    for entry in consultation_queue.to_list():
        print(
            f"{entry['queue_number']} | {entry['patient_id']} | "
            f"{entry['patient_name']} | {entry['illness']} | "
            f"Severity: {entry['severity']} | Priority: {entry['priority']} | "
            f"{entry['status']}"
        )
    print("REAR")


def display_action_stack():
    print()
    print("MEDICAL ACTION HISTORY STACK")

    if medical_action_stack.is_empty():
        print("No medical action has been recorded.")
        return

    print("TOP")
    for action in medical_action_stack.to_list():
        print(f"[{action['timestamp']}] {action['message']}")
    print("BOTTOM")


# ============================================================
#  PATIENT CONSULTATION QUEUING SYSTEM
# ============================================================

def queue_view():
    refresh_queue()
    display_queue("PATIENT CONSULTATION QUEUE (PRIORITY ORDER)")


def queue_view_next():
    refresh_queue()
    entry = consultation_queue.peek()

    print()
    if entry is None:
        print("No patient is currently waiting.")
        return

    print("Next Patient for Consultation:")
    print("Queue Number:", entry["queue_number"])
    print("Patient:", entry["patient_name"])
    print("Illness:", entry["illness"])
    print("Doctor:", entry["doctor"])
    print("Facility:", entry["facility"])
    print("Severity:", entry["severity"])
    print("Priority Level:", entry["priority"])
    print("Status:", entry["status"])


def queue_process_next():
    refresh_queue()
    entry = consultation_queue.peek()

    print()
    if entry is None:
        print("No patient is currently waiting.")
        return

    if entry["status"] == "In Consultation":
        print(f"A consultation is already in progress for {entry['patient_id']}.")
        print("Complete the current consultation first (Medical Action History option 3).")
        return

    record = find_working_record(entry["consultation_id"])
    if record is None:
        print("The consultation record could not be found.")
        return

    print("Next Patient for Consultation:")
    print("Queue Number:", entry["queue_number"])
    print("Patient:", entry["patient_name"])
    print("Illness:", entry["illness"])
    print("Doctor:", entry["doctor"])
    print("Facility:", entry["facility"])
    print("Severity:", entry["severity"])
    print("Priority Level:", entry["priority"])
    print("Status:", entry["status"])

    before = record[:]
    entry["status"] = "In Consultation"
    record[15] = "In Consultation"
    touched_ids.add(record[0])
    push_action(
        "START",
        f"Consultation started for {entry['patient_id']}.",
        before,
        entry
    )
    print("Patient consultation started successfully.")


def queuing_system_menu():
    while True:
        print()
        print("===== Patient Consultation Queuing System =====")
        print("[1] View Patient Consultation Queue")
        print("[2] View Next Patient")
        print("[3] Process Next Patient Consultation")
        print("[4] Exit")

        choice = get_valid_menu_choice("Enter an Option: ", [1, 2, 3, 4])

        if choice == 1:
            queue_view()
        elif choice == 2:
            queue_view_next()
        elif choice == 3:
            queue_process_next()
        else:
            break


# ============================================================
#  MEDICAL ACTION HISTORY
# ============================================================

def get_current_consultation():
    """Returns (queue entry, record) of the consultation in progress."""
    refresh_queue()
    entry = consultation_queue.peek()

    if entry is None or entry["status"] != "In Consultation":
        print()
        print("No consultation is in progress.")
        print("Process the next patient first (Queuing System option 3).")
        return None, None

    record = find_working_record(entry["consultation_id"])
    if record is None:
        print("The consultation record could not be found.")
        return None, None

    print()
    print(f"Current Consultation: {entry['queue_number']} | "
          f"{entry['patient_id']} | {entry['patient_name']}")
    return entry, record


def ma_record_assessment():
    entry, record = get_current_consultation()
    if entry is None:
        return

    assessment = get_record_text("Enter Assessment: ")
    wellness = get_validated_choice("Wellness Status", WELLNESS_STATUSES)
    followup = get_validated_choice("Follow-Up Status", FOLLOWUP_STATUSES)

    before = record[:]
    record[14] = assessment
    record[10] = wellness
    record[9] = followup
    touched_ids.add(record[0])
    push_action(
        "ASSESSMENT",
        f"Assessment recorded for {entry['patient_id']}.",
        before,
        entry
    )

    print("Consultation assessment recorded successfully.")
    display_action_stack()


def ma_update_monitoring():
    entry, record = get_current_consultation()
    if entry is None:
        return

    print("Current Wellness Status:", record[10] or "Not recorded")
    print("Current Follow-Up Status:", record[9] or "Not recorded")
    wellness = get_validated_choice("Wellness Status", WELLNESS_STATUSES)
    followup = get_validated_choice("Follow-Up Status", FOLLOWUP_STATUSES)

    before = record[:]
    record[10] = wellness
    record[9] = followup
    touched_ids.add(record[0])
    push_action(
        "MONITORING",
        f"Monitoring details updated for {entry['patient_id']}.",
        before,
        entry
    )

    print("Patient monitoring details updated successfully.")
    display_action_stack()


def ma_complete_consultation():
    entry, record = get_current_consultation()
    if entry is None:
        return

    if not record[14]:
        print("Record the consultation assessment first (option 1).")
        return

    before = record[:]
    record[15] = "Completed"
    record[16] = get_consultation_datetime()
    touched_ids.add(record[0])

    consultation_queue.dequeue()
    push_action(
        "COMPLETE",
        f"Consultation completed for {entry['patient_id']}.",
        before,
        entry
    )

    print("Patient consultation completed successfully.")
    print(f"Patient {entry['patient_id']} removed from the Consultation Queue.")
    display_queue("UPDATED PATIENT CONSULTATION QUEUE")
    display_action_stack()


def ma_view_stack():
    display_action_stack()


def ma_view_latest():
    latest = medical_action_stack.peek()

    print()
    if latest is None:
        print("No medical action has been recorded.")
        return

    print("Latest Medical Action:")
    print(latest["message"])


def ma_undo_latest():
    latest = medical_action_stack.peek()

    print()
    if latest is None:
        print("No medical action to undo.")
        return

    print("Latest Medical Action:")
    print(latest["message"])
    choice = get_valid_menu_choice("Undo this action? [1] Yes [2] No: ", [1, 2])
    if choice == 2:
        return

    action = medical_action_stack.pop()

    record = find_working_record(action["consultation_id"])
    if record is not None:
        record[:] = action["before"]
        touched_ids.add(record[0])

    persist_changes()
    # The queue rebuilds itself from the restored records.
    refresh_queue()
    print("Action undone successfully.")
    display_queue("PATIENT CONSULTATION QUEUE")
    display_action_stack()


def ma_view_profile_and_history():
    sync_working_consultations()

    print()
    print("===== PATIENT PROFILE AND CONSULTATION HISTORY =====")
    patient = search_patient(prompt_to_add=False, display_result=False)

    if patient is None:
        print("Patient not found.")
        return

    tx_view_patient_profile(patient)
    print_consultation_history(patient[0], working_consultations)


def medical_action_history_menu():
    sync_working_consultations()

    while True:
        print()
        print("===== Medical Action History =====")
        print("[1] Record Consultation Assessment")
        print("[2] Update Patient Monitoring Details")
        print("[3] Complete Current Consultation")
        print("[4] View Medical Action History Stack")
        print("[5] View Latest Medical Action")
        print("[6] Undo Latest Medical Action")
        print("[7] View Patient Profile and Consultation History")
        print("[8] Save Transaction Records")
        print("[9] Exit")

        choice = get_valid_menu_choice("Enter an Option: ", list(range(1, 10)))

        if choice == 1:
            ma_record_assessment()
        elif choice == 2:
            ma_update_monitoring()
        elif choice == 3:
            ma_complete_consultation()
        elif choice == 4:
            ma_view_stack()
        elif choice == 5:
            ma_view_latest()
        elif choice == 6:
            ma_undo_latest()
        elif choice == 7:
            ma_view_profile_and_history()
        elif choice == 8:
            save_transaction_records()
        else:
            prompt_save_if_unsaved()
            break


def main_menu():

    while True:

        print("===== HOSPITAL TRANSACTION SYSTEM =====")
        print("[1] File Maintenance")
        print("[2] Transactions")
        print("[3] View Transactions")
        print("[4] Patient Consultation Queuing System")
        print("[5] Medical Action History")
        print("[6] System Statistics")
        print("[7] View Patient Consultation History")
        print("[8] Exit")

        choice = get_valid_menu_choice("Enter an Option: ", list(range(1, 9)))

        if choice == 1:

            file_maintenance()

        elif choice == 2:

            transaction_menu()

        elif choice == 3:

            view_transactions()

        elif choice == 4:

            queuing_system_menu()

        elif choice == 5:

            medical_action_history_menu()

        elif choice == 6:

            system_statistics()

        elif choice == 7:

            view_patient_history()

        elif choice == 8:
            prompt_save_if_unsaved()
            break

        print()


load_action_history()
main_menu()
