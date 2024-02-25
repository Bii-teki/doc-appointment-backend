from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from faker import Faker
import random
from models import db, Doctor, Patient, DoctorAppointment
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctor_appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)
migrate = Migrate(app, db)


api = Api(app)
fake = Faker()
class Home(Resource):
    def get(self):
        response_message = {
            "message": "Welcome to the Doctors Appointment Management System API"
        }
        return make_response(response_message, 200)

api.add_resource(Home, '/')
class DoctorAPI1(Resource):
    def get(self):
        doctors = []
        for doctor in Doctor.query.all():
            doct_dict = {
                "id": doctor.id,
                "first_name": doctor.first_name,
                "last_name": doctor.last_name,
                "phone_number": doctor.phone_number,
                "username": doctor.username,
                "email": doctor.email,
                "speciality": doctor.speciality,  
                "description": doctor.description,
                "profile": doctor.profile     

            }
            doctors.append(doct_dict)
        return make_response(jsonify(doctors), 200)

api.add_resource(DoctorAPI1, '/doctors1')

class DoctorAPI(Resource):
 


    def get(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if doctor:
            doct_dict = {
                "id": doctor.id,
                "first_name": doctor.first_name,
                "last_name": doctor.last_name,
                "phone_number": doctor.phone_number,
                "username": doctor.username,
                "email": doctor.email,
                "speciality": doctor.speciality                
            }
            
        return make_response(jsonify(doct_dict), 200)


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, help='First name of the doctor', required=True)
        parser.add_argument('last_name', type=str, help='Last name of the doctor', required=True)
        parser.add_argument('username', type=str, help='Username of the doctor', required=True)
        parser.add_argument('email', type=str, help='Email of the doctor', required=True)
        parser.add_argument('speciality', type=str, help='Speciality of the doctor', required=True)
        parser.add_argument('phone_number', type=str, help='Phone number of the doctor', required=True)
        parser.add_argument('address', type=str, help='Address of the doctor', required=True)
        parser.add_argument('password', type=str, help='Password of the doctor', required=True)
        args = parser.parse_args()
        doctor = Doctor(**args)
        db.session.add(doctor)
        db.session.commit()
        return {'message': 'Doctor created successfully'}, 201

    def put(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if doctor:
            parser = reqparse.RequestParser()
            parser.add_argument('first_name', type=str, help='First name of the doctor')
            parser.add_argument('last_name', type=str, help='Last name of the doctor')
            parser.add_argument('username', type=str, help='Username of the doctor')
            parser.add_argument('email', type=str, help='Email of the doctor')
            parser.add_argument('speciality', type=str, help='Speciality of the doctor')
            parser.add_argument('phone_number', type=str, help='Phone number of the doctor')
            parser.add_argument('address', type=str, help='Address of the doctor')
            parser.add_argument('password', type=str, help='Password of the doctor')
            args = parser.parse_args()
            for key, value in args.items():
                if value is not None:
                    setattr(doctor, key, value)
            db.session.commit()
            return {'message': 'Doctor updated successfully'}, 200
        return {'message': 'Doctor not found'}, 404

    def delete(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if doctor:
            db.session.delete(doctor)
            db.session.commit()
            return {'message': 'Doctor deleted successfully'}, 200
        return {'message': 'Doctor not found'}, 404
    
    def patch(self, doctor_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('password', type=str, help='Password')
        args = parser.parse_args()

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {'message': 'Doctor not found'}, 404

        if args['username']:
            doctor.username = args['username']
        if args['password']:
            doctor.password = generate_password_hash(args['password'])

        db.session.commit()
        return {'message': 'Doctor updated successfully'}, 200

api.add_resource(DoctorAPI, '/doctors', '/doctors/<int:doctor_id>')





class DoctorAppointmentAPI(Resource):
    def get(self):
        appoints = []
        for appoint in DoctorAppointment.query.all():
            doct= Doctor.query.get(appoint.doctor_id)
            doct_details ={
                "first_name": doct.first_name,
                "last_name": doct.last_name,
                "phone_number": doct.phone_number,
                "email": doct.email,
                "speciality": doct.speciality
            }

            patient1= Patient.query.get(appoint.patient_id)
            patient1_details ={
                "first_name": patient1.first_name,
                "last_name": patient1.last_name,
                "phone_number": patient1.phone_number,
                "email": patient1.email,
            }

            appoint_dict={
                "Doctor": doct_details,
                "patient": patient1_details,
                "reason": appoint.reason
            }
            appoints.append(appoint_dict)

        if appoints:
            return make_response(jsonify(appoints), 200)
        return {'message': 'No appointments'}, 404
api.add_resource(DoctorAppointmentAPI, '/appointments') 

class DoctorAppointmentAPI2(Resource):
    def get(self, patient_id):
        appoints = []
        for appoint in DoctorAppointment.query.filter_by(patient_id=patient_id).all():
            doct= Doctor.query.get(appoint.doctor_id)
            doct_details ={
                "first_name": doct.first_name,
                "last_name": doct.last_name,
                "phone_number": doct.phone_number,
                "email": doct.email,
                "speciality": doct.speciality
            }

            patient1= Patient.query.get(appoint.patient_id)
            patient1_details ={
                "first_name": patient1.first_name,
                "last_name": patient1.last_name,
                "phone_number": patient1.phone_number,
                "email": patient1.email,
            }

            appoint_dict={
                "Doctor": doct_details,
                "patient": patient1_details,
                "reason": appoint.reason
            }
            appoints.append(appoint_dict)

        if appoints:
            return make_response(jsonify(appoints), 200)
        return {'message': 'No appointments for this patient'}, 404

api.add_resource(DoctorAppointmentAPI2, '/appointments/patient/<int:patient_id>')





class PatientApi(Resource):
    def get(self):
        patients = []
        for patient in Patient.query.all():
            dic_patient ={
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "username": patient.username,
                "phone_number": patient.phone_number,
                "email": patient.email
            }
            patients.append(dic_patient)
        if patients:
            return make_response(jsonify(patients), 200)
        return {'message': 'No patients'}, 404

    def post(self):
        data = request.get_json()
        new_patient = Patient(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('username'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            address=data.get('address'),
            password=data.get('password'),
            role=2  # Assuming 2 is the role for patients
        )
        db.session.add(new_patient)
        db.session.commit()
        return {'message': 'Patient created successfully'}, 201

    def put(self, patient_id):
        data = request.get_json()
        patient = Patient.query.get(patient_id)
        if patient:
            patient.first_name = data.get('first_name', patient.first_name)
            patient.last_name = data.get('last_name', patient.last_name)
            patient.username = data.get('username', patient.username)
            patient.phone_number = data.get('phone_number', patient.phone_number)
            patient.email = data.get('email', patient.email)
            patient.address = data.get('address', patient.address)
            patient.password = data.get('password', patient.password)
            db.session.commit()
            return {'message': 'Patient updated successfully'}, 200
        return {'message': 'Patient not found'}, 404

    def patch(self, patient_id):
        data = request.get_json()
        patient = Patient.query.get(patient_id)
        if patient:
            patient.first_name = data.get('first_name', patient.first_name)
            patient.last_name = data.get('last_name', patient.last_name)
            patient.username = data.get('username', patient.username)
            patient.phone_number = data.get('phone_number', patient.phone_number)
            patient.email = data.get('email', patient.email)
            patient.address = data.get('address', patient.address)
            patient.password = data.get('password', patient.password)
            db.session.commit()
            return {'message': 'Patient updated successfully'}, 200
        return {'message': 'Patient not found'}, 404
        
    def patch(self, patient_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('password', type=str, help='Password')
        args = parser.parse_args()

        patient = Patient.query.get(patient_id)
        if not patient:
            return {'message': 'Patient not found'}, 404

        if args['username']:
            patient.username = args['username']
        if args['password']:
            patient.password = generate_password_hash(args['password'])

        db.session.commit()
        return {'message': 'Patient updated successfully'}, 200

api.add_resource(PatientApi, '/patients', '/patients/<int:patient_id>')



class DoctorAppointmentAPI1(Resource):
    def get(self, doctor_id):
        appoints = []
        for appoint in DoctorAppointment.query.filter_by(doctor_id=doctor_id).all():
            doct = Doctor.query.get(appoint.doctor_id)
            doct_details = {
                "first_name": doct.first_name,
                "last_name": doct.last_name,
                "phone_number": doct.phone_number,
                "email": doct.email,
                "speciality": doct.speciality
            }

            patient1 = Patient.query.get(appoint.patient_id)
            patient1_details = {
                "first_name": patient1.first_name,
                "last_name": patient1.last_name,
                "phone_number": patient1.phone_number,
                "email": patient1.email,
            }

            appoint_dict = {
                "Doctor": doct_details,
                "patient": patient1_details,
                "reason": appoint.reason,
                "appointment_date": str(appoint.appointment_date),  # Convert date to string
                "appointment_time": str(appoint.appointment_time)   # Convert time to string
            }
            appoints.append(appoint_dict)

        if appoints:
            return make_response(jsonify(appoints), 200)
        return {'message': 'No appointments for this doctor'}, 404

api.add_resource(DoctorAppointmentAPI1, '/appointments/doctor/<int:doctor_id>')
                       
class AppointmentApi(Resource):
    def get(self, patient_id=None):
        if patient_id:
            appointments = DoctorAppointment.query.filter_by(patient_id=patient_id).all()
            if not appointments:
                return {'message': 'No appointments found for this patient'}, 404
        else:
            return {'message': 'Patient ID is required'}, 400
    
        appointment_data = []
        for appointment in appointments:
            doctor = Doctor.query.get(appointment.doctor_id)
            if not doctor:
                return {'message': 'Doctor not found'}, 404
            appointment_data.append({
                'id': appointment.id,
                'doctor_id': appointment.doctor_id,
                'doctor_firstname': doctor.first_name,
                'doctor_lastname': doctor.last_name,
                'doctor_email': doctor.email,
                'doctor_phone': doctor.phone_number,
                'patient_id': appointment.patient_id,
                'reason': appointment.reason,
                'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d'),
                'appointment_time': appointment.appointment_time.strftime('%H:%M:%S')
            })
        return {'appointments': appointment_data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('doctor_id', type=int, help='Doctor ID', required=True)
        parser.add_argument('patient_id', type=int, help='Patient ID', required=True)
        parser.add_argument('reason', type=str, help='Reason for appointment', required=True)
        parser.add_argument('appointment_date', type=str, help='Appointment date (YYYY-MM-DD)', required=True)
        parser.add_argument('appointment_time', type=str, help='Appointment time (HH:MM:SS)', required=True)
        args = parser.parse_args()

        doctor_id = args['doctor_id']
        patient_id = args['patient_id']
        reason = args['reason']
        appointment_date = datetime.strptime(args['appointment_date'], '%Y-%m-%d')
        appointment_time = datetime.strptime(args['appointment_time'], '%H:%M:%S').time()

        if not Doctor.query.get(doctor_id):
            return {'message': 'Doctor not found'}, 404

        if not Patient.query.get(patient_id):
            return {'message': 'Patient not found'}, 404

        appointment = DoctorAppointment(
            doctor_id=doctor_id,
            patient_id=patient_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason
        )
        db.session.add(appointment)
        db.session.commit()

        return {'message': 'Appointment created successfully'}, 201

    def patch(self, appointment_id):
        parser = reqparse.RequestParser()
        parser.add_argument('doctor_id', type=int, help='Doctor ID')
        parser.add_argument('patient_id', type=int, help='Patient ID')
        parser.add_argument('reason', type=str, help='Reason for appointment')
        parser.add_argument('appointment_date', type=str, help='Appointment date (YYYY-MM-DD)')
        parser.add_argument('appointment_time', type=str, help='Appointment time (HH:MM:SS)')
        args = parser.parse_args()

        appointment = DoctorAppointment.query.get(appointment_id)
        if not appointment:
            return {'message': 'Appointment not found'}, 404

        if 'doctor_id' in args:
            appointment.doctor_id = args['doctor_id']
        if 'patient_id' in args:
            appointment.patient_id = args['patient_id']
        if 'reason' in args:
            appointment.reason = args['reason']
        if 'appointment_date' in args:
            appointment.appointment_date = datetime.strptime(args['appointment_date'], '%Y-%m-%d')
        if 'appointment_time' in args:
            appointment.appointment_time = datetime.strptime(args['appointment_time'], '%H:%M:%S').time()

        db.session.commit()
        return {'message': 'Appointment updated successfully'}, 200

    def delete(self, appointment_id):
        appointment = DoctorAppointment.query.get(appointment_id)
        if not appointment:
            return {'message': 'Appointment not found'}, 404
        db.session.delete(appointment)
        db.session.commit()
        return {'message': 'Appointment deleted successfully'}, 200

api.add_resource(AppointmentApi, '/appointments', '/appointments/<int:patient_id>', '/appointments/<int:appointment_id>')

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username', required=True)
        parser.add_argument('password', type=str, help='Password', required=True)
        args = parser.parse_args()

        username = args['username']
        password = args['password']

        user = None
        is_doctor = False

        # Check if the user is a doctor
        doctor = Doctor.query.filter_by(username=username).first()
        if doctor:
            user = doctor
            is_doctor = True
        else:
            # Check if the user is a patient
            patient = Patient.query.filter_by(username=username).first()
            if patient:
                user = patient

        if user and check_password_hash(user.password, password):
            user_dict = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "username": user.username,
                "email": user.email,
            }
            if is_doctor:
                user_dict["speciality"] = user.speciality

            return make_response(jsonify({"message": "Logged in successfully", "user": user_dict}), 200)

        return {'message': 'Invalid credentials'}, 401



api.add_resource(Login, '/login')


if __name__ == '__main__':
    app.run(debug=True)
