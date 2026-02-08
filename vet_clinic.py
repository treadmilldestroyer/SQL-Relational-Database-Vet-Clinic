# Here is a program that will work with sqlite to perform various tasks onto a SQL relational database

import sqlite3
import sys
import random
import datetime

DB_name = "vet_clinic.db"

# connects to the database
def db_connection():
    try:
        connect = sqlite3.connect(DB_name) # this creates the vet_clinic.db file or the database file itself
        return connect
    except sqlite3.Error as error:
        print(f"Error connecting to {DB_name}: {error}")
        return None

# write here later what this function does
def create_table(conn):
    cursor = conn.cursor() # the cursor is the tool that executes SQL commands and retrieves results
    
    # the execute code below is SQL code that creates the "patients" table with 6 different columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            PatientID INTEGER PRIMARY KEY AUTOINCREMENT,
            PatientName TEXT,
            AnimalType TEXT,
            PatientAge INT,
            NextAppointment DATE NOT NULL,
            AppointmentDescription TEXT       
        )
    """)
    conn.commit() # this is like hitting the save button in the SQL table


def query_patient(conn):
    cursor = conn.cursor() # the cursor is the tool that executes SQL commands and retrieves results
    print("\n--- View Patients ---")
    print("1. View All Patients")
    print("2. Filter by Date Range")

    choice = input("What would you like to do (1 or 2): ")

    if choice == "2":
        # gets all of the patient records within a specific data range
        print("\n--- Filter by date ---")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        query = """
            SELECT * FROM patients 
            WHERE NextAppointment BETWEEN ? AND ? 
            ORDER BY NextAppointment
        """
        cursor.execute(query, (start_date + " 00:00", end_date + " 23:59"))

    else:
        # gets all of the patient records without any filtering
        cursor.execute("SELECT * FROM patients ORDER BY NextAppointment")

    rows = cursor.fetchall() # gets all of the records in database

    if not rows:
        print("No records found") # in case there are no records in the database, unlikely but good for error catching

    else:
        print(f"\n{"ID":<5} {"Name":<15} {"Animal":<10} {"Next Appointment"}") #formating to create a neat table for visuals
        print("-" * 55)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<10} {row[4]}")
    print("-" * 55)


def add_patient(conn):
    cursor = conn.cursor() # the cursor is the tool that executes SQL commands and retrieves results

    patient_id = random.randint(100000, 999999) # randomizes a 6 digit patient ID number
    pet_name = input("Pet Name: ")
    animal_type = input(f"What kind of animal is {pet_name}: ")
    pet_age = input(f"How old is {pet_name}: ")
    date_input = input("Enter date of next appointment (Format YYYY-MM-DD): ")
    time_input = input("Enter the time of the next appointment (Format HH:MM): ")
    # next_appointment formatted for SQL
    appointment_str = (f"{date_input} {time_input}")
    reason = input("Please explain reason for appointment: ")
    # adds all of the above content into the patients database table in the SQL format
    cursor.execute("""INSERT INTO patients (PatientID, PatientName, AnimalType, PatientAge, 
                   NextAppointment, AppointmentDescription) VALUES (?, ?, ?, ?, ?, ?)""", 
                   (patient_id, pet_name, animal_type, pet_age, appointment_str, reason))

    conn.commit()
    print("Appointment saved.")


def update_patient(conn):
    cursor = conn.cursor() # The tool that executes SQL commands

    print("\n--- Current Patients ---")
    cursor.execute("SELECT PatientID, PatientName FROM patients")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} - Name: {row[1]}")

    # this function will only update one Patient each time this function is called
    # call this function as many times as there are patients you want to update
    patient_id = input("\nEnter the Patient ID to update: ")

    # SQL is difficult so here are two parts that we need to update something
    sql_set_parts = []   
    data_values = []     

    # the while loop will allow us to update as many things as we want to just one Patient ID
    # to update multiple Patient's the user will need to choose the update_patient function more than once
    # once per Patient they want to update
    while True:
        print("\n--- UPDATE ---")
        print("\nWhat would you like to update?")
        print("Options: [name], [type], [age], [appointment], [reason]")
        print("Type 'done' when finished.")
        choice = input("Selection: ").lower()

        if choice == 'done':
            break

        # Check choices and build the lists
        elif choice == 'name':
            new_val = input("Enter new name: ")
            sql_set_parts.append("PatientName = ?")
            data_values.append(new_val)

        elif choice == 'type':
            new_val = input("Enter new animal type: ")
            sql_set_parts.append("AnimalType = ?")
            data_values.append(new_val)

        elif choice == 'age':
            new_val = input("Enter new age: ")
            sql_set_parts.append("PatientAge = ?")
            data_values.append(new_val)

        elif choice == 'appointment':
            # Handle your special Date+Time logic here
            d_input = input("New Date (YYYY-MM-DD): ")
            t_input = input("New Time (HH:MM): ")
            full_date = f"{d_input} {t_input}"
            
            sql_set_parts.append("NextAppointment = ?")
            data_values.append(full_date)

        elif choice == 'reason':
            new_val = input("Enter new reason: ")
            sql_set_parts.append("AppointmentDescription = ?")
            data_values.append(new_val)

        else:
            print("Invalid selection, try again.")

    # Construct and Run the Query
    # Only run if the user actually selected something
    if sql_set_parts:
        # Join the parts with commas: "PatientName = ?, PatientAge = ?"
        set_clause = ", ".join(sql_set_parts)
        
        # Build the final SQL string
        query = f"UPDATE patients SET {set_clause} WHERE PatientID = ?"
        
        # IMPORTANT: Add the ID to the end of the data list for the WHERE clause
        data_values.append(patient_id)
        
        try:
            cursor.execute(query, data_values)
            conn.commit()
            if cursor.rowcount > 0:
                print("Update successful!")
            else:
                print("Error: Patient ID not found.")
        except sqlite3.Error as error:
            print(f"Database Error: {error}")
    else:
        print("No changes made.")


def delete_patient(conn):
    cursor = conn.cursor() # the cursor is the tool that executes SQL commands and retrieves results

    print("\n--- Current Patients ---")
    cursor.execute("SELECT PatientID, PatientName FROM patients")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} - Name: {row[1]}")

    patient_id = input("\nEnter the Patient ID you would like to delete: ")
    cursor.execute("DELETE FROM patients WHERE PatientID = ?", (patient_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("Patient deleted successfully.")
    else:
        print("Error: Patient ID not found.")

# main function is a menu to give an interface for users to perform desired actions on database
def main():
    while True:
        print("\n--- Vet Clinic Database Menu ---")
        print("1. Query a patient")
        print("2. Add a patient")
        print("3. Update a patient")
        print("4. Delete a patient")
        print("5. Exit menu")

        choice = input("Enter the number for the action you would like to do: ")

        if choice == '1':
            query_patient()
        elif choice == '2':
            add_patient()
        elif choice == '3':
            update_patient()
        elif choice == '4':
            delete_patient()
        elif choice == '5':
            break
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()



