import streamlit as st
import mysql.connector

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="password",  # Replace with your MySQL password
        database="HospitalManagement"
    )

# Add a new patient
def add_patient(name, age, gender, contact, address):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Patients (name, age, gender, contact, address)
        VALUES (%s, %s, %s, %s, %s)
    ''', (name, age, gender, contact, address))
    conn.commit()
    conn.close()

# View all patients
def view_patients():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Patients')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Add a new appointment
def add_appointment(patient_id, doctor_id, appointment_date):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Appointments (patient_id, doctor_id, appointment_date)
        VALUES (%s, %s, %s)
    ''', (patient_id, doctor_id, appointment_date))
    conn.commit()
    conn.close()

# Add medical history
def add_medical_history(patient_id, diagnosis, prescription, date):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO MedicalHistory (patient_id, diagnosis, prescription, date)
        VALUES (%s, %s, %s, %s)
    ''', (patient_id, diagnosis, prescription, date))
    conn.commit()
    conn.close()

# View medical history
def view_medical_history(patient_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM MedicalHistory WHERE patient_id = %s', (patient_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def main():
    st.title("Hospital Management System")

    menu = ["Add Patient", "View Patients", "Add Appointment", "Add Medical History", "View Medical History"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Patient":
        st.subheader("Add New Patient")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        contact = st.text_input("Contact")
        address = st.text_input("Address")
        if st.button("Add Patient"):
            add_patient(name, age, gender, contact, address)
            st.success("Patient Added Successfully!")

    elif choice == "View Patients":
        st.subheader("Patient Records")
        patients = view_patients()
        for patient in patients:
            st.write(f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}, Gender: {patient[3]}, Contact: {patient[4]}, Address: {patient[5]}")

    elif choice == "Add Appointment":
        st.subheader("Add New Appointment")
        patient_id = st.number_input("Patient ID", min_value=1)
        doctor_id = st.number_input("Doctor ID", min_value=1)
        appointment_date = st.date_input("Appointment Date")
        if st.button("Add Appointment"):
            add_appointment(patient_id, doctor_id, appointment_date)
            st.success("Appointment Added Successfully!")

    elif choice == "Add Medical History":
        st.subheader("Add Medical History")
        patient_id = st.number_input("Patient ID", min_value=1)
        diagnosis = st.text_area("Diagnosis")
        prescription = st.text_area("Prescription")
        date = st.date_input("Date")
        if st.button("Add Medical History"):
            add_medical_history(patient_id, diagnosis, prescription, date)
            st.success("Medical History Added Successfully!")

    elif choice == "View Medical History":
        st.subheader("View Medical History")
        patient_id = st.number_input("Patient ID", min_value=1)
        if st.button("View History"):
            history = view_medical_history(patient_id)
            for record in history:
                st.write(f"Record ID: {record[0]}, Diagnosis: {record[2]}, Prescription: {record[3]}, Date: {record[4]}")

if __name__ == "__main__":
    main()
