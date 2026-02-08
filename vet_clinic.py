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

# what does this function do?
def create_table(conn):
    cursor = conn.cursor()
    
    # the execute code below is SQL code that creates the "patients" table
    # with 6 different columns
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

def add_patient(conn):
    cursor = conn.cursor()

    patient_id = random.randint(000000, 999999)
    pet_name = input("Pet Name: ")
    animal_type = input(f"What kind of animal is {pet_name}: ")
    pet_age = input(f"How old is {pet_name}: ")

    #generate a date and store it as the Next Appointment (create this function if time permits)
    days_ahead = random.randint(1,30)
    appt_hour = random.randint(8, 16)
    today = datetime.datetime.now()
    future_date = today + datetime.timedelta(days=days_ahead)
    next_appointment = future_date.replace(hour=appt_hour, minute=0, second=0, microsecond=0)
    # next_appointment formatted for SQL
    appointment_str = next_appointment.strftime("%Y-%m-%d %H:%M")

    reason = input("Please explain reason for appointment: ")



    cursor.execute("""INSERT INTO patients (PatientID, PatientName, AnimalType, PatientAge, 
                   NextAppointment, AppointmentDescription) VALUES (?, ?, ?, ?, ?, ?)""", (patient_id, pet_name, animal_type, pet_age, appointment_str, reason))

    conn.commit()
    print("Appointment saved.")