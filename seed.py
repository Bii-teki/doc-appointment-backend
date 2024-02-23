from app import app, db
from faker import Faker
from models import Doctor, DoctorAppointment, Patient
from datetime import datetime
import random

fake = Faker()

with app.app_context():
    db.create_all()  # Create all tables

    def delete_data():
        print("🦸 Delete_data...")
        Doctor.query.delete()
        Patient.query.delete()
        DoctorAppointment.query.delete()

    def seed_data():
        print("🦸‍♀️ Seeding Doctors...")
        specialties = [
            "Cardiology", "Dermatology", "Endocrinology", "Gastroenterology",
            "Hematology", "Neurology", "Oncology", "Pediatrics", "Psychiatry",
            "Rheumatology", "Urology", "Orthopedics", "Ophthalmology", "Otolaryngology"
        ]

        for _ in range(5):  # Generate 5 fake doctors
            doctor = Doctor(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                username=fake.user_name(),
                email=fake.email(),
                address=fake.address(),
                password=fake.password(),
                phone_number=fake.phone_number(),
                speciality=random.choice(specialties),
                profile=fake.image_url(),
                description=fake.text(max_nb_chars=200),
                role=1  # Assuming 1 is the role for doctors
            )
            db.session.add(doctor)

        print("🦸‍♀️ Seeding Patients...")
        for _ in range(50):  # Generate 50 fake patients
            patient = Patient(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                username=fake.user_name(),
                email=fake.email(),
                address=fake.address(),
                password=fake.password(),
                phone_number=fake.phone_number(),
                role=2  # Assuming 2 is the role for patients
            )
            db.session.add(patient)

        db.session.commit()

        print("🦸‍♀️ Seeding Doctor Appointments...")
        doctors = Doctor.query.all()
        patients = Patient.query.all()
        
        for doctor in doctors:
            for _ in range(10):  # Each doctor has 10 appointments
                patient = fake.random_element(patients)
                appointment_datetime = fake.date_time_between(start_date='now', end_date='+1y')
                appointment_date = appointment_datetime.date()
                appointment_time = appointment_datetime.time()

                appointment = DoctorAppointment(
                    doctor_id=doctor.id,
                    patient_id=patient.id,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    reason=fake.sentence()
                )
                db.session.add(appointment)

        db.session.commit()

    if __name__ == "__main__":
        seed_data()
        print("🦸‍♀️ Done seeding!")
