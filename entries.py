# from faker import Faker
# from random import randint
# from models import db, SchoolDetails, GradeDetails, StudentDetails, ParentDetails, PaymentDetails

# def add_entries():
#     fake = Faker()

#     # Generate and add 100 entries to the School_Details table
#     for _ in range(100):
#         school = SchoolDetails(
#             Name=fake.company(),
#             City=fake.city(),
#             Address=fake.address(),
#             PrincipalName=fake.name(),
#             PrincipalPhone=fake.phone_number(),
#             PrincipalEmail=fake.email(),
#             AdminName=fake.name(),
#             AdminPhone=fake.phone_number(),
#             AdminEmail=fake.email()
#         )
#         db.session.add(school)

#     # Generate and add 100 entries to the Grade_Details table
#     for _ in range(100):
#         grade = GradeDetails(
#             School_ID=randint(1, 100),  # Assuming schools have IDs from 1 to 100
#             className=randint(1, 12),  # Assuming class names range from 1 to 12
#             FeeAmount=randint(1000, 5000)  # Assuming fee amount ranges from 1000 to 5000
#         )
#         db.session.add(grade)

#     # Generate and add 100 entries to the Student_Details table
#     for _ in range(100):
#         student = StudentDetails(
#             SchoolID=randint(1, 100),  # Assuming schools have IDs from 1 to 100
#             className=randint(1, 12),  # Assuming class names range from 1 to 12
#             FirstName=fake.first_name(),
#             MiddleName=fake.first_name(),
#             LastName=fake.last_name(),
#             DOB=fake.date_of_birth(minimum_age=6, maximum_age=18),  # Assuming students' age range from 6 to 18
#             parent_id=randint(1, 100)  # Assuming parent IDs range from 1 to 100
#         )
#         db.session.add(student)

#     # Generate and add 100 entries to the Parent_Details table
#     for _ in range(100):
#         parent = ParentDetails(
#             Name=fake.name(),
#             mobileno=fake.phone_number(),
#             email=fake.email()
#         )
#         db.session.add(parent)

#     # Generate and add 100 entries to the Payment_Details table
#     for _ in range(100):
#         payment = PaymentDetails(
#             school_id=randint(1, 100),  # Assuming schools have IDs from 1 to 100
#             student_id=randint(1, 100),  # Assuming student IDs range from 1 to 100
#             class_id=randint(1, 100),  # Assuming class IDs range from 1 to 100
#             Fees=randint(1000, 5000),  # Assuming fee amount ranges from 1000 to 5000
#             status=fake.random_element(elements=('Paid', 'Unpaid'))  # Randomly select 'Paid' or 'Unpaid'
#         )
#         db.session.add(payment)

#     # Commit changes to the database
#     db.session.commit()
