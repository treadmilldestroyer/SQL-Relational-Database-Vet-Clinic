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

    pet_name = input("Pet Name: ")
    animal_type = input(f"What kind of animal is {pet_name}: ")
    pet_age = input(f"How old is {pet_name}: ")

    #generate a date and store it as the Next Appointment


    reason = input("Please explain reason for appointment: ")

