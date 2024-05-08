# models.py
from flask_sqlalchemy import SQLAlchemy
import random
 
db = SQLAlchemy()

class SchoolDetails(db.Model):
    __tablename__ = 'School_Details'
    ID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(200), unique = True, nullable = False)
    City = db.Column(db.String(100), nullable = False)
    Address = db.Column(db.String(100), nullable = False)
    PrincipalName = db.Column(db.String(100), nullable = False)
    PrincipalPhone = db.Column(db.String(10), unique = True, nullable = False)
    PrincipalEmail = db.Column(db.String(50), unique = True, nullable = False)
    AdminName = db.Column(db.String(100), nullable = False)
    AdminPhone = db.Column(db.String(10), unique = True, nullable = False)
    AdminEmail = db.Column(db.String(59), unique = True, nullable = False)
    password = db.Column(db.String(4), nullable = False)

    def __str__(self):
        return self.Name

class GradeDetails(db.Model):
    __tablename__ = 'Grade_Details' 
    ID = db.Column(db.Integer, primary_key = True)
    School_ID = db.Column(db.Integer, db.ForeignKey('School_Details.ID'), nullable = False)
    className = db.Column(db.Integer, nullable = False)
    FeeAmount = db.Column(db.Float, nullable = False)

class StudentDetails(db.Model):
    __tablename__ = 'Student_Details'
    ID = db.Column(db.Integer, primary_key = True)
    SchoolID = db.Column(db.Integer, db.ForeignKey('School_Details.ID'), nullable = False)
    className = db.Column(db.Integer, nullable = False)
    FirstName = db.Column(db.String(50), nullable = False)
    MiddleName = db.Column(db.String(50), nullable = False)
    LastName = db.Column(db.String(50), nullable = False)
    parent_id = db.Column(db.Integer, db.ForeignKey('Parent_Details.ID'))

    def __init__(self, SchoolID, className, FirstName, MiddleName, LastName, parent_id):
        self.SchoolID = SchoolID 
        self.className = className
        self.FirstName = FirstName
        self.MiddleName = MiddleName
        self.LastName = LastName
        self.parent_id = parent_id
        self.generate_id()

    def generate_id(self):
        while True:
            new_id = random.randint(100000, 999999)

            existing_user = ParentDetails.query.filter_by(ID = new_id).first()

            if not existing_user:
                self.ID = new_id
                break


class ParentDetails(db.Model):
    __tablename__ = 'Parent_Details'
    ID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String, nullable = False)
    mobileno = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(4), nullable = False)

    def __init__(self, Name, mobileno, email, password):
        self.Name = Name
        self.mobileno = mobileno
        self.email = email
        self.password = password
        self.generate_id()

    def generate_id(self):
        while True:
            new_id = random.randint(100000, 999999)

            existing_user = ParentDetails.query.filter_by(ID = new_id).first()

            if not existing_user:
                self.ID = new_id
                break

class PaymentDetails(db.Model):
    __tablename__ = 'Payment_Details'
    ID = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('School_Details.ID'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('Student_Details.ID'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('Grade_Details.ID'), nullable=False)
    Fees = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)