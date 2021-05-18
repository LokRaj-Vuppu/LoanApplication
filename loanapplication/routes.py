import os
import random
from flask import render_template, request, redirect, url_for, flash, make_response
from loanapplication import app, db, bcrypt 
# docimages
from loanapplication.models import customer, employee, loan_details, ApplyLoan, loan_status, user_datastore, User
# from loanapplication.forms import RegistrationForm, LoginForm
# from flask_login import login_user, current_user, logout_user, login_required
from datetime import date, time
from loanapplication import mail
from flask_mail import Message
from flask_mail import *
from flask_security import roles_accepted,roles_required, login_required, login_user, logout_user, current_user

import pdfkit
# from celery import delay


@app.route('/')
def home():
    return render_template('home.html', title='Home')


#Login and Regustration

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = customer(customer_name=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)
#
#
#
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = customer.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)


@app.route('/addroleadmin')
def addrole():
    admin_role=user_datastore.find_or_create_role('admin')
    user_datastore.add_role_to_user(current_user,admin_role)
    db.session.commit()
    return '<h1>role assigned to admin</h1>'


@app.route('/addrolecustomer')
def addrolecustomer():
    customer_role=user_datastore.find_or_create_role('customer')
    user_datastore.add_role_to_user(current_user,customer_role)
    db.session.commit()
    return '<h1>role assigned to customer</h1>'


@app.route('/addroleexecute')
def addroleexecutive():
    executive_role=user_datastore.find_or_create_role('executive')
    user_datastore.add_role_to_user(current_user,executive_role)
    db.session.commit()
    return '<h1>role assigned to executive</h1>'




@app.route('/customerhome')
@login_required
@roles_accepted('admin','customer')
def customerhome():
    data = customer.query.all()
    return render_template('customerhome.html', customerdata=data, title='Customer Details')


@app.route('/withoutadmin')
@login_required
@roles_accepted('admin','customer')
def withoutadmin():
    mail = current_user.email
    data = customer.query.filter_by(email=mail).first()
    return render_template('withoutadmin.html', customerdata=data, title='Customer Details')



#Adding skill data
@app.route('/add_customer', methods=['POST'])
@roles_accepted('admin','customer')
def add_customer():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        customer_name = request.form['customer_name']
        phone = request.form['phone']
        mail = request.form['mail']
        dob = request.form['dob']
        gender = request.form['gender']
        address = request.form['address']
        occupation = request.form['occupation']
        annual_income = request.form['annual_income']


        customerdata = customer(customer_id, customer_name, phone,
                                mail, dob, gender, address,
                                occupation, annual_income)
        db.session.add(customerdata)
        db.session.commit()
        flash('Data Added successfully')
        return redirect(url_for('customerhome'))

#Deleting skill data
@app.route('/delete_customer/<id>', methods=['POST', 'GET'])
def delete_customer(id):
    customerdata = customer.query.filter_by(customer_id = id).first()
    db.session.delete(customerdata)
    db.session.commit()
    flash('Data Removed Successfully')
    return redirect(url_for('customerhome'))

# for editing the data
@app.route('/edit_customer/<id>', methods=['POST', 'GET'])
@roles_accepted('customer')
def edit_customer(id):
    customerdata = customer.query.filter_by(customer_id = id).first()
    return render_template('editcustomer.html', data=customerdata, title='Edit Customer')

#for updating the data
@app.route('/update_customer/<id>', methods=['POST'])
def update_customer(id):
    customerdata = customer.query.filter_by(customer_id =id).first()
    if request.method == "POST":
        if customerdata:
            customer_id = request.form['customer_id']
            customer_name = request.form['customer_name']
            phone = request.form['phone']
            email = request.form['mail']
            dob = request.form['dob']
            gender = request.form['gender']
            address = request.form['address']
            occupation = request.form['occupation']
            annual_income = request.form['annual_income']

            customerdata.customer_id = customer_id
            customerdata.customer_name = customer_name
            customerdata.phone = phone
            customerdata.email = email
            customerdata.dob = dob
            customerdata.gender = gender
            customerdata.address = address
            customerdata.occupation = occupation
            customerdata.annual_income = annual_income

            db.session.commit()
        flash('Data Updated Successfully')
    return redirect(url_for('withoutadmin'))

#CRUD Operations for EMPLOYEE Model

@app.route('/employeehome')
@login_required
@roles_accepted('admin','executive')
def employeehome():
    data = employee.query.all()
    return render_template('employeehome.html',employeedata = data, title='Employee Details')


@app.route('/homeadmin')
@login_required
@roles_accepted('admin','executive')
def homeadmin():
    mail = current_user.email
    data = employee.query.filter_by(emp_email=mail).first()
    return render_template('homeadmin.html',employeedata = data, title='Employee Details')



# Adding Employee data
@app.route('/add_employee', methods=['POST'])
@roles_accepted('admin','executive')
def add_employee():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        employee_name = request.form['employee_name']
        emp_phone = request.form['emp_phone']
        emp_email = request.form['emp_email']
        designation = request.form['designation']


        employeedata = employee(employee_id, employee_name, emp_phone,
                                emp_email, designation)
        db.session.add(employeedata)
        db.session.commit()
        flash('Data Added successfully', 'success')
        return redirect(url_for('employeehome'))

#Deleting skill data
@app.route('/delete_employee/<id>', methods=['POST', 'GET'])
@roles_accepted('admin')
def delete_employee(id):
    employeedata = employee.query.filter_by(employee_id = id).first()
    db.session.delete(employeedata)
    db.session.commit()
    flash('Data Removed Successfully', 'success')
    return redirect(url_for('employeehome'))

# for editing the data
@app.route('/edit_employee/<id>', methods=['POST', 'GET'])
@roles_accepted('executive')
def edit_employee(id):
    employeedata = employee.query.filter_by(employee_id = id).first()
    return render_template('editemployee.html', data=employeedata, title='Edit Employee')

#for updating the data
@app.route('/update_employee/<id>', methods=['POST'])
@roles_accepted('executive')
def update_employee(id):
    employeedata = employee.query.filter_by(employee_id =id).first()
    if request.method == "POST":
        if employeedata:
            employee_id = request.form['employee_id']
            employee_name = request.form['employee_name']
            emp_phone = request.form['emp_phone']
            emp_email = request.form['emp_email']
            designation = request.form['designation']

            employeedata.employee_id = employee_id
            employeedata.employee_name = employee_name
            employeedata.emp_phone = emp_phone
            employeedata.emp_email = emp_email
            employeedata.designation = designation

            db.session.commit()
        flash('Data Updated Successfully', 'success')
    return redirect(url_for('homeadmin'))


# for editing the data from dashboard
@app.route('/edit_loan_data/<id>', methods=['POST', 'GET'])
@login_required
@roles_accepted('admin')
def edit_loan_data(id):
    loandata = loan_status.query.filter_by(statusid = id).first()
    return render_template('edit_loandata.html', data=loandata, title='Edit Loan Data')

#for updating the data from dashboard
@app.route('/update_loan_data/<id>', methods=['POST'])
@roles_accepted('admin')
def update_loan_data(id):
    loandata = loan_status.query.filter_by(statusid =id).first()
    if request.method == "POST":
        if loandata:
            statusid = request.form['statusid']
            employee_id = request.form['employee_id']
            customer_name = request.form['customer_name']
            email = request.form['email']
            loan_id = request.form['loan_id']
            loan_type = request.form['loan_type']
            date_approval = request.form['date_approval']
            status = request.form['status']
            amount_sanctioned = request.form['amount_sanctioned']
            tenure = request.form['tenure']
            feedback = request.form['feedback']

            loandata.date_approval = date_approval
            loandata.status = status
            loandata.amount_sanctioned = amount_sanctioned
            loandata.tenure = tenure
            loandata.feedback = feedback
            db.session.commit()

            # data = loan_status.query.filter_by(statusid=statusid).first()
            # rendered = render_template('status.html', data=data)
            # pdf = pdfkit.from_string(rendered, False)
            # response = make_response(pdf)
            # response.headers['content-Type'] = 'application/pdf'
            # response.headers['content-Disposition'] = 'attachment; filename=out.pdf'


            msg = Message("Your Loan Application is "+loandata.status, sender='yourId@gmail.com', recipients=[email])
            # if loandata.status == 'Approved':
            msg.subject = "Your Loan Application is "+loandata.status
            msg.body = "Your Loan Application is "+loandata.status+". Kindly find the detailed loan report in below attached document."

            with app.open_resource('report.pdf') as fp:
                msg.attach('report.pdf', "application/pdf", fp.read())
            # else:
            #     msg.body = "Your Loan Application is "+loandata.status+". Kindly find the detailed loan report in below attached document."
            #
            #     with app.open_resource('report.pdf') as fp:
            #         msg.attach('report.pdf', "application/pdf", fp.read())
            mail.send(msg)

        flash('Data Updated Successfully', 'success')
        # return redirect(url_for('send_mail'))
    return redirect(url_for('dashboard'))

@app.route('/send_mail/<id>')
def send_mail(id):
    data = loan_status.query.filter_by(statusid = id).first()
    rendered = render_template('status.html',data=data)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['content-Type'] = 'application/pdf'
    response.headers['content-Disposition'] = 'attachment; filename=report.pdf'
    os.remove("C:/Users/lokra/PycharmProjects/LoanApplication/loanapplication/report.pdf")
    return response


@app.route('/apply_loan', methods=['GET','POST'])
@login_required
@roles_accepted('customer')
def apply_loan():
    loan_id = random.randint(1,1000000)
    # if customer_data:
    user_data = User.query.filter_by(email = current_user.email).first()
    customer_data = customer.query.filter_by(email = user_data.email).first()
    if request.method == 'POST':
        loan_id = request.form['loanid']
        customer_id = request.form['customer_id']
        customer_name = request.form['customer_name']
        email = request.form['email']
        loan_type = request.form['loantype']
        amount_needed = request.form['amount']
        pan = docimages.save(request.files['PAN'])
        aadhar = docimages.save(request.files['aadhar'])
        passport = docimages.save(request.files['passport'])
        panloc = docimages.url(pan)
        aadharloc = docimages.url(aadhar)
        passportloc = docimages.url(passport)
        apply_date = date.today()
        status = "waiting"
        employee_id = None
        new_loan = ApplyLoan(loan_id, customer_id,employee_id,customer_name, email, loan_type, amount_needed, status, panloc, aadharloc,passportloc, apply_date)
        db.session.add(new_loan)
        db.session.commit()
        flash('Data Updated Successfully')
        return redirect(url_for('apply_loan'))
    return render_template("applyloan.html", title='Loan Application', loan_id=loan_id, customer_data=customer_data)



@app.route('/dashboard')
@login_required
@roles_accepted('admin','executive')
def dashboard():
    loandetails = loan_status.query.all()
    car=loan_status.query.filter_by(loan_type='car').count()
    home = loan_status.query.filter_by(loan_type='home').count()
    personal = loan_status.query.filter_by(loan_type='personal').count()
    approved = loan_status.query.filter_by(status='Approved').count()
    waiting = loan_status.query.filter_by(status='waitlisted').count()
    rejected = loan_status.query.filter_by(status='Rejected').count()
    return render_template('dashboard.html',title='Dashboard', car=car,home=home,personel=personal,approved=approved,waiting=waiting,rejected=rejected, loandetails=loandetails)





@app.route("/loanstatusdata",methods=["GET","POST"])
def loanstatusdata():
    loandetails=loan_status.query.all()
    return render_template('loandetails.html', title='Application', loandetails=loandetails)



@app.route("/check_status", methods=["GET", "POST"])
def check_status():
    if request.method == "POST":
        loan_id = request.form['id']
        loandata = loan_status.query.filter_by(loan_id=loan_id).first()
        applyloandata = ApplyLoan.query.filter_by(loan_id=loan_id).first()
        if loandata:
            return render_template('status.html', data=loandata)
        elif applyloandata:
            flash('Your Loan Application is still under verification','info')
        else:
            flash('Invalid Loan ID', 'danger')
    return render_template('checkstatus.html', title='Application Status')


# @app.route('/applications')
# def applications():
#     loandata = ApplyLoan.query.all()
#     return render_template('applications.html',title='Applications', loandata=loandata)


@app.route('/approveloan/<id>', methods=["GET"])
def approveloan(id):
    statusid = random.randint(1, 900000)
    loan = ApplyLoan.query.filter_by(loan_id=id).first()
    return render_template('approve.html', data=loan, title='Verification',statusid=statusid)


@app.route("/loanstatus", methods=["POST"])
def loanstatus():
    status_id = request.form['statusid']
    employee_id = request.form['employee_id']
    customer_name = request.form['customer_name']
    email = request.form['email']
    loan_id = request.form['loan_id']
    loan_type = request.form['type']
    date_approval = request.form['date_approval']
    status = request.form['status']
    amount_sanctioned = request.form['amount_sanctioned']
    tenure = request.form['tenure']
    feedback = request.form['feedback']
    loandata = ApplyLoan.query.filter_by(loan_id=loan_id).first()
    loandata.status = status
    statement = loan_status(status_id,employee_id,customer_name,email,loan_id,loan_type,date_approval,status,amount_sanctioned,tenure,feedback)
    db.session.add(statement)
    db.session.commit()
    return redirect(url_for('applications'))



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=["GET","POST"])
@login_required
def account():
    customer_name = current_user.customer_name
    email = current_user.email
    customerdata = customer.query.filter_by(customer_name=customer_name).first()
    if request.method == "POST":
        current_user.customer_name = request.form['customer_name']
        current_user.phone = request.form['phone']

        current_user.dob = request.form['dob']
        current_user.gender = request.form['gender']
        current_user.address = request.form['address']
        current_user.occupation = request.form['occupation']
        current_user.annual_income = request.form['annual_income']

        db.session.commit()
        flash('Your account has been updated!', 'success')

    return render_template('account.html', title='Account', customerdata=customerdata)


@app.route('/applicationsemployee')
@login_required
@roles_accepted('admin')
def applicationsemployee():
    loandata=ApplyLoan.query.all()
    return render_template('applicationsemployee.html',loandata=loandata)


@app.route('/assignemployee',methods=['GET','POST'])
@login_required
@roles_accepted('admin')
def assign():
    loanid = request.form['loan_id']
    empid = request.form['employee_id']
    loandetails = ApplyLoan.query.filter_by(loan_id=loanid).first()
    loandetails.employee_id = empid
    loandetails.status = "assigned"
    db.session.commit()
    return render_template("assignapplications.html",loandata=loandetails)


@app.route('/applications')
@login_required
@roles_accepted('executive')
def applications():
    current_email = current_user.email
    current_employee = employee.query.filter_by(emp_email=current_email).first()
    loandata = ApplyLoan.query.filter_by(employee_id=current_employee.employee_id).all()
    return render_template('applications.html',loandata=loandata)


@app.route('/loanapplications/<id>')
@login_required
@roles_accepted('admin')
def loanapplications(id):
    # custname = current_user.name
    loandata = ApplyLoan.query.filter_by(loan_id=id).first()
    empdata = employee.query.all()
    return render_template('assignapplications.html',loandata=loandata,empdata=empdata)



