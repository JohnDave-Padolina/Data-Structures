import tkinter as tk
from tkinter import ttk, messagebox

# =========================================================
# FILE SETTINGS
# =========================================================

file_name = "doctors.txt"


# =========================================================
# COLORS
# Change these values to adjust the entire design
# =========================================================

PRIMARY = "#1565C0"
DARK_BLUE = "#0D47A1"
LIGHT_BLUE = "#E3F2FD"
BACKGROUND = "#F4F8FC"
WHITE = "#FFFFFF"
TEXT = "#263238"
GRAY = "#607D8B"
SUCCESS = "#2E7D32"
DANGER = "#C62828"
WARNING = "#EF6C00"


# =========================================================
# ROOT WINDOW
# =========================================================

root = tk.Tk()

root.title("J2A Hospital - Doctor Management System")
root.geometry("1100x700")
root.minsize(900, 600)
root.configure(bg=BACKGROUND)


# =========================================================
# TKINTER STYLES
# =========================================================

style = ttk.Style()
style.theme_use("clam")

# General buttons
style.configure(
    "Custom.TButton",
    font=("Segoe UI", 11),
    padding=(15, 10),
    background=PRIMARY,
    foreground=WHITE,
    borderwidth=0
)

style.map(
    "Custom.TButton",
    background=[
        ("active", DARK_BLUE)
    ],
    foreground=[
        ("active", WHITE)
    ]
)

# Green button
style.configure(
    "Success.TButton",
    font=("Segoe UI", 11),
    padding=(15, 10),
    background=SUCCESS,
    foreground=WHITE
)

style.map(
    "Success.TButton",
    background=[
        ("active", "#1B5E20")
    ]
)

# Red button
style.configure(
    "Danger.TButton",
    font=("Segoe UI", 11),
    padding=(15, 10),
    background=DANGER,
    foreground=WHITE
)

style.map(
    "Danger.TButton",
    background=[
        ("active", "#8E0000")
    ]
)

# Labels
style.configure(
    "Title.TLabel",
    font=("Segoe UI", 28, "bold"),
    foreground=PRIMARY,
    background=BACKGROUND
)

style.configure(
    "Subtitle.TLabel",
    font=("Segoe UI", 13),
    foreground=GRAY,
    background=BACKGROUND
)

style.configure(
    "Heading.TLabel",
    font=("Segoe UI", 22, "bold"),
    foreground=TEXT,
    background=BACKGROUND
)

style.configure(
    "Normal.TLabel",
    font=("Segoe UI", 11),
    foreground=TEXT,
    background=BACKGROUND
)

# Entry
style.configure(
    "Custom.TEntry",
    font=("Segoe UI", 11),
    padding=8
)

# Combobox
style.configure(
    "Custom.TCombobox",
    font=("Segoe UI", 11),
    padding=8
)

# Treeview
style.configure(
    "Treeview",
    font=("Segoe UI", 10),
    rowheight=35,
    background=WHITE,
    fieldbackground=WHITE,
    foreground=TEXT
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold"),
    background=PRIMARY,
    foreground=WHITE,
    padding=8
)

style.map(
    "Treeview",
    background=[
        ("selected", "#90CAF9")
    ],
    foreground=[
        ("selected", TEXT)
    ]
)


# =========================================================
# FILE FUNCTIONS
# =========================================================

def create_file():

    try:
        file = open(file_name, "r")
        file.close()

    except FileNotFoundError:

        new_file = open(file_name, "w")
        new_file.close()


def read_all_records():

    create_file()

    all_records = []

    file = open(file_name, "r")

    for line in file:

        line = line.strip()

        parts = line.split(" | ")

        if len(parts) == 4:
            all_records.append(parts)

    file.close()

    return all_records


def save_all_records(records):

    file = open(file_name, "w")

    for record in records:

        name = record[0]
        contact = record[1]
        specialization = record[2]
        category = record[3]

        file.write(
            f"{name} | {contact} | "
            f"{specialization} | {category}\n"
        )

    file.close()


def get_matching_records(specialization, category):

    matches = []

    all_records = read_all_records()

    for record in all_records:

        if (
            record[2] == specialization
            and record[3] == category
        ):
            matches.append(record)

    return matches


# =========================================================
# CLEAR WINDOW
# =========================================================

def clear_window():

    for widget in root.winfo_children():
        widget.destroy()


# =========================================================
# HEADER
# =========================================================

def create_header(title, subtitle=None):

    header = tk.Frame(
        root,
        bg=BACKGROUND
    )

    header.pack(
        fill="x",
        padx=40,
        pady=(30, 10)
    )

    tk.Label(
        header,
        text=title,
        font=("Segoe UI", 24, "bold"),
        fg=PRIMARY,
        bg=BACKGROUND
    ).pack()

    if subtitle:

        tk.Label(
            header,
            text=subtitle,
            font=("Segoe UI", 11),
            fg=GRAY,
            bg=BACKGROUND
        ).pack(pady=(5, 0))


# =========================================================
# CARD
# =========================================================

def create_card(parent, title, description, command):

    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground="#D5DDE5",
        highlightthickness=1
    )

    card.pack(
        fill="x",
        padx=20,
        pady=8
    )

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 14, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 2)
    )

    tk.Label(
        card,
        text=description,
        font=("Segoe UI", 10),
        fg=GRAY,
        bg=WHITE
    ).pack(
        anchor="w",
        padx=20
    )

    ttk.Button(
        card,
        text="Open",
        style="Custom.TButton",
        command=command
    ).pack(
        anchor="e",
        padx=20,
        pady=15
    )

    return card


# =========================================================
# MAIN MENU
# =========================================================

def main_menu():

    clear_window()

    create_header(
        "🏥 J2A HOSPITAL",
        "Doctor Management System"
    )

    container = tk.Frame(
        root,
        bg=BACKGROUND
    )

    container.pack(
        fill="both",
        expand=True,
        padx=150,
        pady=30
    )

    create_card(
        container,
        "👨‍⚕️ Admin",
        "Manage doctor records.",
        admin_menu
    )

    create_card(
        container,
        "👤 User",
        "View available doctors.",
        user_menu
    )

    create_card(
        container,
        "✕ Close Program",
        "Exit the application.",
        root.destroy
    )


# =========================================================
# ADMIN MENU
# =========================================================

def admin_menu():

    clear_window()

    create_header(
        "Admin Dashboard",
        "Select a doctor category"
    )

    container = tk.Frame(
        root,
        bg=BACKGROUND
    )

    container.pack(
        fill="both",
        expand=True,
        padx=150
    )

    create_card(
        container,
        "🩺 Medical and Organ Specialist",
        "Manage medical and organ specialists.",
        medical_organ_specialist_admin
    )

    create_card(
        container,
        "🧑‍⚕️ Primary Care",
        "Manage primary care doctors.",
        primary_care_admin
    )

    create_card(
        container,
        "🏥 Surgical Specialist",
        "Manage surgical specialists.",
        surgical_specialist_admin
    )

    ttk.Button(
        root,
        text="← Back",
        style="Custom.TButton",
        command=main_menu
    ).pack(pady=20)


# =========================================================
# USER MENU
# =========================================================

def user_menu():

    clear_window()

    create_header(
        "Welcome To J2A Hospital",
        "Find a doctor"
    )

    container = tk.Frame(
        root,
        bg=BACKGROUND
    )

    container.pack(
        fill="both",
        expand=True,
        padx=150
    )

    create_card(
        container,
        "🩺 Medical and Organ Specialist",
        "View medical and organ specialists.",
        medical_organ_specialist_user
    )

    create_card(
        container,
        "🧑‍⚕️ Primary Care",
        "View primary care doctors.",
        primary_care_user
    )

    create_card(
        container,
        "🏥 Surgical Specialist",
        "View surgical specialists.",
        surgical_specialist_user
    )

    ttk.Button(
        root,
        text="← Back",
        style="Custom.TButton",
        command=main_menu
    ).pack(pady=20)


# =========================================================
# ADMIN SPECIALIZATION MENUS
# =========================================================

def medical_organ_specialist_admin():

    specialization_menu(
        "Medical and Organ Specialist",
        [
            "Cardiologists",
            "Dermatologists",
            "Neurologists"
        ],
        True
    )


def primary_care_admin():

    specialization_menu(
        "Primary Care",
        [
            "Physicians",
            "Pediatricians",
            "Internists"
        ],
        True
    )


def surgical_specialist_admin():

    specialization_menu(
        "Surgical Specialist",
        [
            "General Surgeons",
            "Orthopedic Surgeons",
            "Obstetricians and Gynecologists"
        ],
        True
    )


# =========================================================
# USER SPECIALIZATION MENUS
# =========================================================

def medical_organ_specialist_user():

    specialization_menu(
        "Medical and Organ Specialist",
        [
            "Cardiologists",
            "Dermatologists",
            "Neurologists"
        ],
        False
    )


def primary_care_user():

    specialization_menu(
        "Primary Care",
        [
            "Physicians",
            "Pediatricians",
            "Internists"
        ],
        False
    )


def surgical_specialist_user():

    specialization_menu(
        "Surgical Specialist",
        [
            "General Surgeons",
            "Orthopedic Surgeons",
            "Obstetricians and Gynecologists"
        ],
        False
    )


# =========================================================
# SPECIALIZATION MENU
# =========================================================

def specialization_menu(category, specializations, is_admin):

    clear_window()

    create_header(
        category,
        "Select a specialization"
    )

    container = tk.Frame(
        root,
        bg=BACKGROUND
    )

    container.pack(
        fill="both",
        expand=True,
        padx=150
    )

    for specialization in specializations:

        if is_admin:

            command = lambda s=specialization: crud_menu(
                s,
                category
            )

        else:

            command = lambda s=specialization: view_records_window(
                s,
                category,
                False
            )

        create_card(
            container,
            specialization,
            "Select this specialization.",
            command
        )

    back_command = admin_menu if is_admin else user_menu

    ttk.Button(
        root,
        text="← Back",
        style="Custom.TButton",
        command=back_command
    ).pack(pady=20)


# =========================================================
# CRUD MENU
# =========================================================

def crud_menu(specialization, category):

    clear_window()

    create_header(
        specialization,
        category
    )

    container = tk.Frame(
        root,
        bg=BACKGROUND
    )

    container.pack(
        fill="both",
        expand=True,
        padx=150
    )

    create_card(
        container,
        "➕ Add Record",
        "Add a new doctor.",
        lambda: add_record_window(
            specialization,
            category
        )
    )

    create_card(
        container,
        "📋 View Records",
        "View all doctors.",
        lambda: view_records_window(
            specialization,
            category,
            True
        )
    )

    create_card(
        container,
        "✏ Update Record",
        "Update an existing doctor.",
        lambda: update_record_window(
            specialization,
            category
        )
    )

    create_card(
        container,
        "🗑 Delete Record",
        "Delete an existing doctor.",
        lambda: delete_record_window(
            specialization,
            category
        )
    )

    ttk.Button(
        root,
        text="← Back",
        style="Custom.TButton",
        command=admin_menu
    ).pack(pady=20)


# =========================================================
# ADD RECORD
# =========================================================

def add_record_window(specialization, category):

    clear_window()

    create_header(
        "Add Doctor",
        f"{specialization} - {category}"
    )

    form = tk.Frame(
        root,
        bg=WHITE,
        highlightbackground="#D5DDE5",
        highlightthickness=1
    )

    form.pack(
        padx=250,
        pady=30,
        fill="x"
    )

    tk.Label(
        form,
        text="Doctor Name",
        font=("Segoe UI", 11, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 5)
    )

    name_entry = ttk.Entry(
        form,
        style="Custom.TEntry"
    )

    name_entry.pack(
        fill="x",
        padx=30
    )

    tk.Label(
        form,
        text="Contact Number",
        font=("Segoe UI", 11, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(
        anchor="w",
        padx=30,
        pady=(20, 5)
    )

    contact_entry = ttk.Entry(
        form,
        style="Custom.TEntry"
    )

    contact_entry.pack(
        fill="x",
        padx=30
    )

    def save_record():

        name = name_entry.get().strip()
        contact = contact_entry.get().strip()

        if name == "" or contact == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter the doctor's name and contact number."
            )

            return

        all_records = read_all_records()

        new_record = [
            name,
            contact,
            specialization,
            category
        ]

        all_records.append(new_record)

        save_all_records(all_records)

        messagebox.showinfo(
            "Success",
            f'Record for "{name}" added successfully.'
        )

        crud_menu(
            specialization,
            category
        )

    ttk.Button(
        form,
        text="Save Record",
        style="Success.TButton",
        command=save_record
    ).pack(
        pady=25
    )

    ttk.Button(
        root,
        text="← Back",
        style="Custom.TButton",
        command=lambda: crud_menu(
            specialization,
            category
        )
    ).pack(pady=15)


# =========================================================
# VIEW RECORDS
# =========================================================

def view_records_window(
    specialization,
    category,
    is_admin
):

    clear_window()

    create_header(
        "Doctor Records",
        f"{specialization} - {category}"
    )

    container = tk.Frame(
        root,
        bg=BACKGROUND
    )

    container.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=10
    )

    columns = (
        "ID",
        "Doctor Name",
        "Contact",
        "Specialization",
        "Category"
    )

    tree = ttk.Treeview(
        container,
        columns=columns,
        show="headings"
    )

    tree.heading(
        "ID",
        text="ID"
    )

    tree.heading(
        "Doctor Name",
        text="Doctor Name"
    )

    tree.heading(
        "Contact",
        text="Contact"
    )

    tree.heading(
        "Specialization",
        text="Specialization"
    )

    tree.heading(
        "Category",
        text="Category"
    )

    tree.column(
        "ID",
        width=50,
        anchor="center"
    )

    tree.column(
        "Doctor Name",
        width=200
    )

    tree.column(
        "Contact",
        width=150
    )

    tree.column(
        "Specialization",
        width=220
    )

    tree.column(
        "Category",
        width=220
    )

    scrollbar = ttk.Scrollbar(
        container,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    matches = get_matching_records(
        specialization,
        category
    )

    for index, record in enumerate(
        matches,
        start=1
    ):

        tree.insert(
            "",
            "end",
            values=(
                index,
                record[0],
                record[1],
                record[2],
                record[3]
            )
        )

    if len(matches) == 0:

        tk.Label(
            container,
            text="No records found.",
            font=("Segoe UI", 12),
            fg=GRAY,
            bg=BACKGROUND
        ).pack(pady=20)

    if is_admin:

        back_command = lambda: crud_menu(
            specialization,
            category
        )

    else:

        back_command = lambda: specialization_menu(
            category,
            get_specializations(category),
            False
        )

    ttk.Button(
        root,
        text="← Back",
        style="Custom.TButton",
        command=back_command
    ).pack(pady=20)


# =========================================================
# GET SPECIALIZATIONS
# =========================================================

def get_specializations(category):

    if category == "Medical and Organ Specialist":

        return [
            "Cardiologists",
            "Dermatologists",
            "Neurologists"
        ]

    elif category == "Primary Care":

        return [
            "Physicians",
            "Pediatricians",
            "Internists"
        ]

    elif category == "Surgical Specialist":

        return [
            "General Surgeons",
            "Orthopedic Surgeons",
            "Obstetricians and Gynecologists"
        ]

    return []


# =========================================================
# UPDATE RECORD
# =========================================================

def update_record_window(
    specialization,
    category
):

    matches = get_matching_records(
        specialization,
        category
    )

    if len(matches) == 0:

        messagebox.showinfo(
            "No Records",
            "There are no records to update."
        )

        return

    clear_window()

    create_header(
        "Update Doctor",
        f"{specialization} - {category}"
    )

    form = tk.Frame(
        root,
        bg=WHITE,
        highlightbackground="#D5DDE5",
        highlightthickness=1
    )

    form.pack(
        padx=250,
        pady=30,
        fill="x"
    )

    tk.Label(
        form,
        text="Select Doctor",
        font=("Segoe UI", 11, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 5)
    )

    doctor_names = [
        record[0]
        for record in matches
    ]

    doctor_box = ttk.Combobox(
        form,
        values=doctor_names,
        state="readonly",
        style="Custom.TCombobox"
    )

    doctor_box.pack(
        fill="x",
        padx=30
    )

    tk.Label(
        form,
        text="New Doctor Name",
        font=("Segoe UI", 11, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(
        anchor="w",
        padx=30,
        pady=(20, 5)
    )

    name_entry = ttk.Entry(
        form,
        style="Custom.TEntry"
    )

    name_entry.pack(
        fill="x",
        padx=30
    )

    tk.Label(
        form,
        text="New Contact Number",
        font=("Segoe UI", 11, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(
        anchor="w",
        padx=30,
        pady=(20, 5)
    )

    contact_entry = ttk.Entry(
        form,
        style="Custom.TEntry"
    )

    contact_entry.pack(
        fill="x",
        padx=30
    )

    def update():

        selected_name = doctor_box.get()

        if selected_name == "":

            messagebox.showwarning(
                "Select Doctor",
                "Please select a doctor."
            )

            return

        new_name = name_entry.get().strip()
        new_contact = contact_entry.get().strip()

        if new_name == "" and new_contact == "":

            messagebox.showwarning(
                "No Changes",
                "Please enter a new name or contact number."
            )

            return

        all_records = read_all_records()

        for record in all_records:

            if (
                record[0] == selected_name
                and record[2] == specialization
                and record[3] == category
            ):

                if new_name != "":
                    record[0] = new_name

                if new_contact != "":
                    record[1] = new_contact

                break

        save_all_records(all_records)

        messagebox.showinfo(
            "Success",
            "Doctor record updated successfully."
        )

        crud_menu(
            specialization,
            category
        )

    ttk.Button(
        form,
        text="Update Record",
        style="Success.TButton",
        command=update
    ).pack(
        pady=25
    )

    ttk.Button(
        root,
        text="← Back",
        style="Custom.TButton",
        command=lambda: crud_menu(
            specialization,
            category
        )
    ).pack(pady=15)


# =========================================================
# DELETE RECORD
# =========================================================

def delete_record_window(
    specialization,
    category
):

    matches = get_matching_records(
        specialization,
        category
    )

    if len(matches) == 0:

        messagebox.showinfo(
            "No Records",
            "There are no records to delete."
        )

        return

    clear_window()

    create_header(
        "Delete Doctor",
        f"{specialization} - {category}"
    )

    form = tk.Frame(
        root,
        bg=WHITE,
        highlightbackground="#D5DDE5",
        highlightthickness=1
    )

    form.pack(
        padx=250,
        pady=30,
        fill="x"
    )

    tk.Label(
        form,
        text="Select Doctor",
        font=("Segoe UI", 11, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 5)
    )

    doctor_names = [
        record[0]
        for record in matches
    ]

    doctor_box = ttk.Combobox(
        form,
        values=doctor_names,
        state="readonly",
        style="Custom.TCombobox"
    )

    doctor_box.pack(
        fill="x",
        padx=30
    )

    def delete():

        selected_name = doctor_box.get()

        if selected_name == "":

            messagebox.showwarning(
                "Select Doctor",
                "Please select a doctor."
            )

            return

        confirmation = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete "
            f'"{selected_name}"?'
        )

        if not confirmation:
            return

        all_records = read_all_records()

        record_to_delete = None

        for record in all_records:

            if (
                record[0] == selected_name
                and record[2] == specialization
                and record[3] == category
            ):

                record_to_delete = record
                break

        if record_to_delete is None:

            messagebox.showerror(
                "Error",
                "Record could not be found."
            )

            return

        all_records.remove(
            record_to_delete
        )

        save_all_records(
            all_records
        )

        messagebox.showinfo(
            "Success",
            "Doctor record deleted successfully."
        )

        crud_menu(
            specialization,
            category
        )

    ttk.Button(
        form,
        text="Delete Record",
        style="Danger.TButton",
        command=delete
    ).pack(
        pady=25
    )

    ttk.Button(
        root,
        text="← Back",
        style="Custom.TButton",
        command=lambda: crud_menu(
            specialization,
            category
        )
    ).pack(pady=15)


# =========================================================
# START PROGRAM
# =========================================================

create_file()

main_menu()

root.mainloop()
