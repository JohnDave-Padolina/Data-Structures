import datetime

DOCTORS_FILE = 'doctors.txt'
PATIENTS_FILE = 'patients.txt'
ILLNESS_FILE = 'illnesses.txt'
HOSPITAL_FILE = 'hospitals.txt'
CLINIC_FILE = 'clinics.txt'
CONSULT_FILE = 'consultations.txt'

SEVERITY_LEVELS = ['Mild', 'Moderate', 'Severe']
PRIORITY_LEVELS = ['Low', 'Medium', 'High']
CARE_TYPES = ['Hospital', 'Barangay Health Center']
FOLLOWUP_STATUSES = ['Required', 'Not Required', 'Completed']
WELLNESS_STATUSES = ['Improving', 'Stable', 'Critical', 'Recovered']


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


def save_records(filename, records):
    with open(filename, 'w') as file:
        for record in records:
            file.write(' | '.join(record) + '\n')


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


def add_patient():
    patients = read_records(PATIENTS_FILE, 5)

    print()
    print("===== ADD PATIENT =====")

    patient_id = input("Enter Patient ID: ").strip()
    name = input("Enter Patient Name: ").strip()
    age = get_valid_age()
    address = input("Enter Address: ").strip()
    contact = input("Enter Contact Number: ").strip()

    patient = [
        patient_id,
        name,
        str(age),
        address,
        contact
    ]

    patients.append(patient)
    save_records(PATIENTS_FILE, patients)

    print("Patient added successfully.")
    print()


def view_patients():
    patients = read_records(PATIENTS_FILE, 5)

    print()
    print("===== PATIENT LIST =====")

    if not patients:
        print("No patient records found.")
        print()
        return

    for count, patient in enumerate(patients, start=1):
        print(f"[{count}] ID: {patient[0]}")
        print(f"    Name: {patient[1]}")
        print(f"    Age: {patient[2]}")
        print(f"    Address: {patient[3]}")
        print(f"    Contact: {patient[4]}")
        print()


def search_patient():
    patients = read_records(PATIENTS_FILE, 5)

    print()
    print("===== SEARCH PATIENT =====")

    patient_id = input("Enter Patient ID: ").strip()

    for patient in patients:
        if patient[0] == patient_id:
            print()
            print("Patient Found")
            print("ID:", patient[0])
            print("Name:", patient[1])
            print("Age:", patient[2])
            print("Address:", patient[3])
            print("Contact:", patient[4])
            print()
            return patient

    print("Patient not found.")
    print()
    return None


def add_doctor():
    doctors = read_records(DOCTORS_FILE, 4)

    print()
    print("===== ADD DOCTOR =====")

    doctor_id = input("Enter Doctor ID: ").strip()
    name = input("Enter Doctor Name: ").strip()
    specialization = input("Enter Specialization: ").strip()
    contact = input("Enter Contact Number: ").strip()

    doctor = [
        doctor_id,
        name,
        specialization,
        contact
    ]

    doctors.append(doctor)
    save_records(DOCTORS_FILE, doctors)

    print("Doctor added successfully.")
    print()


def view_doctors():
    doctors = read_records(DOCTORS_FILE, 4)

    print()
    print("===== DOCTOR LIST =====")

    if not doctors:
        print("No doctor records found.")
        print()
        return

    for count, doctor in enumerate(doctors, start=1):
        print(f"[{count}] Doctor ID: {doctor[0]}")
        print(f"    Name: {doctor[1]}")
        print(f"    Specialization: {doctor[2]}")
        print(f"    Contact: {doctor[3]}")
        print()


def add_hospital():
    hospitals = read_records(HOSPITAL_FILE, 2)

    print()
    print("===== ADD HOSPITAL / BARANGAY HEALTH CENTER =====")

    name = input("Enter Name: ").strip()

    care_type = get_validated_choice(
        "Care Type",
        CARE_TYPES
    )

    hospitals.append([
        name,
        care_type
    ])

    save_records(HOSPITAL_FILE, hospitals)

    print("Hospital / Barangay Health Center added successfully.")
    print()


def view_hospitals():
    hospitals = read_records(HOSPITAL_FILE, 2)

    print()
    print("===== HOSPITAL / BARANGAY HEALTH CENTER LIST =====")

    if not hospitals:
        print("No records found.")
        print()
        return

    for count, hospital in enumerate(hospitals, start=1):
        print(f"[{count}] {hospital[0]}")
        print(f"    Care Type: {hospital[1]}")
        print()


def add_clinic():
    clinics = read_records(CLINIC_FILE, 2)

    print()
    print("===== ADD SPECIALTY CLINIC =====")

    clinic_name = input("Enter Clinic Name: ").strip()
    specialization = input("Enter Linked Specialization: ").strip()

    clinics.append([
        clinic_name,
        specialization
    ])

    save_records(CLINIC_FILE, clinics)

    print("Specialty Clinic added successfully.")
    print()


def view_clinics():
    clinics = read_records(CLINIC_FILE, 2)

    print()
    print("===== SPECIALTY CLINIC LIST =====")

    if not clinics:
        print("No specialty clinics found.")
        print()
        return

    for count, clinic in enumerate(clinics, start=1):
        print(f"[{count}] {clinic[0]}")
        print(f"    Specialization: {clinic[1]}")
        print()


def add_illness():
    illnesses = read_records(ILLNESS_FILE, 3)

    print()
    print("===== ADD ILLNESS =====")

    illness_name = input("Enter Illness Name: ").strip()

    severity = get_validated_choice(
        "Severity",
        SEVERITY_LEVELS
    )

    priority = get_validated_choice(
        "Priority",
        PRIORITY_LEVELS
    )

    illnesses.append([
        illness_name,
        severity,
        priority
    ])

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
        print(f"[{count}] Illness: {illness[0]}")
        print(f"    Severity: {illness[1]}")
        print(f"    Priority: {illness[2]}")
        print()


def file_maintenance():
    while True:
        print("===== FILE MAINTENANCE =====")
        print("[1] Add Patient")
        print("[2] View Patients")
        print("[3] Add Doctor")
        print("[4] View Doctors")
        print("[5] Add Hospital / Barangay Health Center")
        print("[6] View Hospitals / Barangay Health Centers")
        print("[7] Add Specialty Clinic")
        print("[8] View Specialty Clinics")
        print("[9] Add Illness")
        print("[10] View Illnesses")
        print("[11] Return")

        choice = get_valid_menu_choice("Enter an Option: ", list(range(1, 12)))

        if choice == 1:
            add_patient()
        elif choice == 2:
            view_patients()
        elif choice == 3:
            add_doctor()
        elif choice == 4:
            view_doctors()
        elif choice == 5:
            add_hospital()
        elif choice == 6:
            view_hospitals()
        elif choice == 7:
            add_clinic()
        elif choice == 8:
            view_clinics()
        elif choice == 9:
            add_illness()
        elif choice == 10:
            view_illnesses()
        elif choice == 11:
            break

        print()


def tx_search_patient():
    return search_patient()


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


def tx_select_doctor():
    doctors = read_records(DOCTORS_FILE, 4)

    print()
    print("===== SELECT DOCTOR =====")

    if not doctors:
        print("No doctors available.")
        print()
        return None

    for count, doctor in enumerate(doctors, start=1):
        print(f"[{count}] {doctor[1]} - {doctor[2]}")

    choice = get_valid_menu_choice("Enter an Option: ", list(range(1, len(doctors) + 1)))

    selected = doctors[choice - 1]

    print("Selected Doctor:", selected[1])
    print()

    return selected[1]


def tx_select_hospital():
    hospitals = read_records(HOSPITAL_FILE, 2)

    print()
    print("===== SELECT HOSPITAL / BARANGAY HEALTH CENTER =====")

    if not hospitals:
        print("No hospital or health center available.")
        print()
        return None

    for count, hospital in enumerate(hospitals, start=1):
        print(f"[{count}] {hospital[0]} - {hospital[1]}")

    choice = get_valid_menu_choice("Enter an Option: ", list(range(1, len(hospitals) + 1)))

    selected = hospitals[choice - 1]

    print("Selected:", selected[0])
    print()

    return selected[0]


def tx_select_clinic():
    print()
    print("===== SPECIALTY CLINIC =====")
    print("[1] Yes")
    print("[2] No")

    needs_clinic = get_valid_menu_choice("Enter an Option: ", [1, 2])

    if needs_clinic == 2:
        print("Specialty Clinic skipped.")
        print()
        return None

    clinics = read_records(CLINIC_FILE, 2)

    if not clinics:
        print("No specialty clinics available.")
        print()
        return None

    print()
    print("===== SELECT SPECIALTY CLINIC =====")

    for count, clinic in enumerate(clinics, start=1):
        print(f"[{count}] {clinic[0]} - {clinic[1]}")

    choice = get_valid_menu_choice("Enter an Option: ", list(range(1, len(clinics) + 1)))

    selected = clinics[choice - 1]

    print("Selected Clinic:", selected[0])
    print()

    return selected[0]


def tx_select_or_record_illness():
    print()
    print("===== ILLNESS SELECTION =====")
    print("[1] Select Existing Illness")
    print("[2] Record New Illness")

    choice = get_valid_menu_choice("Enter an Option: ", [1, 2])

    illnesses = read_records(ILLNESS_FILE, 3)

    if choice == 1:

        if not illnesses:
            print("No illness records available.")
            print()
            return None

        print()
        print("===== SELECT ILLNESS =====")

        for count, illness in enumerate(illnesses, start=1):
            print(
                f"[{count}] {illness[0]} "
                f"(Severity: {illness[1]}, Priority: {illness[2]})"
            )

        selected = get_valid_menu_choice("Enter an Option: ", list(range(1, len(illnesses) + 1)))

        illness = illnesses[selected - 1]

        print("Selected Illness:", illness[0])
        print()

        return {
            "name": illness[0],
            "severity": illness[1],
            "priority": illness[2]
        }

    else:

        print()
        print("===== RECORD NEW ILLNESS =====")

        illness_name = input("Enter Illness Name: ").strip()

        severity = get_validated_choice(
            "Severity",
            SEVERITY_LEVELS
        )

        priority = get_validated_choice(
            "Priority",
            PRIORITY_LEVELS
        )

        illnesses.append([
            illness_name,
            severity,
            priority
        ])

        save_records(ILLNESS_FILE, illnesses)

        print("New illness recorded.")
        print()

        return {
            "name": illness_name,
            "severity": severity,
            "priority": priority
        }


def tx_record_consultation_details(transaction):

    print()
    print("===== CONSULTATION DETAILS =====")

    transaction["followup"] = get_validated_choice(
        "Follow-up Status",
        FOLLOWUP_STATUSES
    )

    transaction["wellness"] = get_validated_choice(
        "Wellness Status",
        WELLNESS_STATUSES
    )

    print()
    
    list(transaction["date"].strftime("%c"))
    #transaction_date = input("Enter Consultation Date: ").strip()
    #transaction_time = input("Enter Consultation Time: ").strip()

    if transaction_date == '' or transaction_time == '':
        print("Date and time cannot be empty.")
        print()
        return False

    #transaction["date"] = transaction_date + " " + transaction_time
    transaction["date"] = datetime.datetime.now()



    print()
    print("Consultation details recorded.")
    print()

    return True


def tx_save_transaction(transaction):

    required_fields = [
        "patient",
        "doctor",
        "hospital",
        "illness_name",
        "severity",
        "priority",
        "followup",
        "wellness",
        "date"
    ]

    for field in required_fields:

        if field not in transaction:
            print("Transaction is incomplete.")
            print("Missing:", field)
            print()
            return

    consultations = read_records(CONSULT_FILE, 12)

    consultation_id = str(len(consultations) + 1)

    patient = transaction["patient"]

    record = [
        consultation_id,
        patient[0],
        patient[1],
        transaction["doctor"],
        transaction["hospital"],
        transaction.get("clinic") or "N/A",
        transaction["illness_name"],
        transaction["severity"],
        transaction["priority"],
        transaction["followup"],
        transaction["wellness"],
        transaction["date"]
    ]

    consultations.append(record)

    save_records(CONSULT_FILE, consultations)

    print("Transaction saved successfully.")
    print("Consultation ID:", consultation_id)
    print()


def transaction_menu():

    transaction = {}

    while True:

        print("===== TRANSACTION =====")
        print("[1] Search Patient")
        print("[2] View Patient Profile")
        print("[3] Select Doctor")
        print("[4] Select Hospital or Barangay Health Center")
        print("[5] Select Specialty Clinic, if applicable")
        print("[6] Select or Record Illness Information")
        print("[7] Record Patient Consultation")
        print("[8] Save Transaction")
        print("[9] Return to Main Menu")

        choice = get_valid_menu_choice("Enter an Option: ", list(range(1, 10)))

        if choice == 1:

            patient = tx_search_patient()

            if patient:
                transaction["patient"] = patient

        elif choice == 2:

            patient = transaction.get("patient")

            tx_view_patient_profile(patient)

        elif choice == 3:

            doctor = tx_select_doctor()

            if doctor:
                transaction["doctor"] = doctor

        elif choice == 4:

            hospital = tx_select_hospital()

            if hospital:
                transaction["hospital"] = hospital

        elif choice == 5:

            clinic = tx_select_clinic()

            transaction["clinic"] = clinic

        elif choice == 6:

            illness = tx_select_or_record_illness()

            if illness:
                transaction["illness_name"] = illness["name"]
                transaction["severity"] = illness["severity"]
                transaction["priority"] = illness["priority"]

        elif choice == 7:

            tx_record_consultation_details(transaction)

        elif choice == 8:

            tx_save_transaction(transaction)

        elif choice == 9:

            break

        print()


def view_transactions():

    consultations = read_records(CONSULT_FILE, 12)

    print()
    print("===== TRANSACTION RECORDS =====")

    if not consultations:
        print("No transaction records found.")
        print()
        return

    for count, record in enumerate(consultations, start=1):

        print(f"===== TRANSACTION {count} =====")
        print("Consultation ID:", record[0])
        print("Patient ID:", record[1])
        print("Patient Name:", record[2])
        print("Doctor:", record[3])
        print("Hospital:", record[4])
        print("Clinic:", record[5])
        print("Illness:", record[6])
        print("Severity:", record[7])
        print("Priority:", record[8])
        print("Follow-Up:", record[9])
        print("Wellness:", record[10])
        print("Date and Time:", record[11])
        print()


def system_statistics():

    patients = read_records(PATIENTS_FILE, 5)
    doctors = read_records(DOCTORS_FILE, 4)
    hospitals = read_records(HOSPITAL_FILE, 2)
    clinics = read_records(CLINIC_FILE, 2)
    illnesses = read_records(ILLNESS_FILE, 3)
    consultations = read_records(CONSULT_FILE, 12)

    print()
    print("===== SYSTEM STATISTICS =====")
    print("Total Patients:", len(patients))
    print("Total Doctors:", len(doctors))
    print("Total Hospitals / Health Centers:", len(hospitals))
    print("Total Specialty Clinics:", len(clinics))
    print("Total Illness Records:", len(illnesses))
    print("Total Consultations:", len(consultations))
    print()


def main_menu():

    while True:

        print("===== Medical Information System  =====")
        print("[1] File Maintenance")
        print("[2] Transaction")
        print("[3] View Transaction")
        print("[4] System Statistics")
        print("[5] Exit")

        choice = get_valid_menu_choice("Enter an Option: ", list(range(1, 6)))

        if choice == 1:

            file_maintenance()

        elif choice == 2:

            transaction_menu()

        elif choice == 3:

            view_transactions()

        elif choice == 4:

            system_statistics()

        elif choice == 5:

            print("Closing program...")
            break

        print()


main_menu()
