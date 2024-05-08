from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from models import db, ParentDetails, StudentDetails, PaymentDetails, GradeDetails, SchoolDetails
from config import Config
import psycopg2
import requests
import base64
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

if not app.config.get('SQLALCHEMY_DATABASE_URI'):
    raise ValueError('DATABASE_URL is not set. Please make sure to set this environment variable.')

def get_db_connection():
    return psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])

# Function to calculate SHA-256 hash
def calculate_sha256_string(input_string):
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    sha256.update(input_string.encode('utf-8'))
    return sha256.finalize().hex()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = ParentDetails.query.filter_by(email=username).first()

        if user and user.password == password:
            session['username'] = username
            return redirect('/parentDash')
        else:
            return redirect('/login')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']

        try:
            new_user = ParentDetails(Name=name, mobileno=mobile, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html')
        except Exception as e:
            print("Error occurred while adding user:", str(e))
            return render_template('error.html', error=str(e))

@app.route('/parentDash')
def parentDash():
    try:
        username = session.get('username')
        if username is None:
            return render_template('error.html', error="Username not provided.")

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(""" 
            SELECT "ID" FROM "Parent_Details" WHERE email = %s
        """, (username,))

        parent_id = cursor.fetchone()

        if parent_id:
            cursor.execute("""
                SELECT sd."SchoolID", sd."ID", sd."FirstName", sd."LastName", sd."className", pd."Fees", pd."status" FROM "Student_Details" sd LEFT JOIN "Payment_Details" pd ON sd."ID" = pd."student_id" WHERE sd."parent_id" = %s 
             """, (parent_id,))
            student_data = cursor.fetchall()
            cursor.close()
            connection.close()
            print(student_data)
            return render_template('parentDash.html', student_data=student_data)
        else:
            return render_template('error.html', error="Parent not found.")

    except Exception as e:
        print(" Error occurred while  fetching  parent and   students data : ", str(e))
        return render_template('error.html', error=str(e))

@app.route('/parentProfile')
def parentProfile():
    return render_template('parentProfile.html')

@app.route('/paymentHistory')
def paymentHistory():
    return render_template('paymentHistory.html')

@app.route('/children')
def children():
    schools = SchoolDetails.query.all()
    sch = [(school.Name, school.ID) for school in schools]

    grades = GradeDetails.query.all()
    gr = [grade.className for grade in grades]

    print(sch)
    print(gr)

    try:
        username = session.get('username')
        if username is None:
            return render_template('error.html', error = "Username not provided.")
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(""" 
            SELECT "ID" FROM "Parent_Details" WHERE email = %s
        """, (username,))

        parent_id = cursor.fetchone()

        if parent_id:
            cursor.execute("""
                SELECT sd."SchoolID", sd."ID", sd."FirstName", sd."MiddleName",sd."LastName", sd."className" FROM "Student_Details" sd WHERE sd."parent_id" = %s 
             """, (parent_id,))
            student_data = cursor.fetchall()
            cursor.close()
            connection.close()
            print(student_data)
            return render_template('children.html', student_data = student_data, schools=schools, grades=grades, sch=sch, gr=gr)
        else:
            return render_template('error.html', error = "Parent not found.")
        
    except Exception as e:
        print(" Error occurred while  fetching  parent and   students data : ", str(e))
        return render_template('error.html', error = str(e))   

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/addchild', methods=["POST"])
def addchild():
    if request.method == 'POST':
        email = session.get('username')
        parent = ParentDetails.query.filter_by(email = email).first()

        if parent:
            parent_id = parent.ID
        else:
            return "error"
        
       
        fname = request.form['FirstName']
        mname = request.form['MiddleName']
        lname = request.form['LastName']
        schooln = request.form['schoolname']
        classn = request.form['classname']
        schid = request.form['schoolid']

        print(fname, mname,lname, schooln, classn, schid)

        existing_student = StudentDetails.query.filter_by(FirstName=fname, parent_id=parent_id).first()

        if existing_student:
            return "Error: A student with the same first name and parent ID already exists."

        school = SchoolDetails.query.filter_by(Name = schooln).first()
        if school:
            school_id = school.ID
        else:
            return "Error: School Not Found" 
        
        new_student = StudentDetails(SchoolID = school_id, className = classn, FirstName = fname, MiddleName = mname, LastName = lname, parent_id = parent_id)

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('children'))

@app.route('/pay', methods=['POST'])
def pay():
    # Parse the JSON payload sent by the frontend
    data = request.json
    amount_entered = data.get('amount')

    # Check if the 'amount' key is present in the payload
    if amount_entered is None:
        return jsonify({'error': 'Amount not provided in request'}), 400

    # Construct the main payload for payment
    MAINPAYLOAD = {
        "merchantId": "PGTESTPAYUAT",
        "merchantTransactionId": shortuuid.uuid(),
        "merchantUserId": "MUID123",
        "amount": int(amount_entered) * 100,
        "redirectUrl": "http://127.0.0.1:5000/return-to-me",
        "redirectMode": "POST",
        "callbackUrl": "http://127.0.0.1:5000/return-to-me",
        "mobileNumber": "9999999999",
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }

    # Additional parameters for checksum calculation
    INDEX = "1"
    ENDPOINT = "/pg/v1/pay"
    SALTKEY = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"

    # Generate checksum for request verification
    base64String = base64.b64encode(json.dumps(MAINPAYLOAD).encode('utf-8')).decode('utf-8')
    mainString = base64String + ENDPOINT + SALTKEY
    sha256Val = calculate_sha256_string(mainString)
    checkSum = sha256Val + '###' + INDEX

    # Set headers for the request
    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': checkSum,
        'accept': 'application/json',
    }

    # Send payment request to the payment gateway
    json_data = {'request': base64String}
    response = requests.post('https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay', headers=headers, json=json_data)
    responseData = response.json()

    # Return success response
    return jsonify({'status': 'Payment request received', 'amount': amount_entered}), 200

@app.route('/return-to-me', methods=['POST'])
def return_to_me():
    # Extract necessary data from the form data
    transaction_id = request.form.get("transactionId")

    # Additional parameters for checksum calculation
    INDEX = "1"
    SALTKEY = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"

    # Perform necessary actions with the transaction ID (e.g., query payment status)
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    request_url = f'https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/PGTESTPAYUAT/{transaction_id}'
    sha256_payload_string = f'/pg/v1/status/PGTESTPAYUAT/{transaction_id}{SALTKEY}'
    sha256_val = calculate_sha256_string(sha256_payload_string)
    checksum = f'{sha256_val}###{INDEX}'

    # Set headers for the request
    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': checksum,
        'X-MERCHANT-ID': transaction_id,
        'accept': 'application/json',
    }

    # Make request to get payment status
    response = requests.get(request_url, headers=headers)
    checkout_response = response.json()

    # Extract payment details
    payment_details = {
        "amount": checkout_response['data']['amount'],
        # Add other payment details as needed
    }

    # Return success response
    return jsonify({'message': 'Return from payment gateway', 'payment_details': payment_details}), 200

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()
    app.run(debug=True)