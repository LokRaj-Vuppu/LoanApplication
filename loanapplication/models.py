from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, login_manager
from flask_security import RoleMixin, SQLAlchemyUserDatastore, Security, UserMixin

from loanapplication import db, app

# login_manager


# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))


# class User(db.Model, UserMixin):
#     userid = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30))
#     email = db.Column(db.String(50))
#     password = db.Column(db.String(100))

    # def get_id(self):
    #     return self.userid



# loan = db.Table('loan',
#     db.Column('employee_id', db.Integer, db.ForeignKey('employee.employee_id')), #primary_key=True),
#     db.Column('customer_id', db.Integer, db.ForeignKey('customer.customer_id')), #primary_key=True),
#     db.Column('loan_id',db.String(40)),
#     db.Column('loan_type',db.String(40)),
#     db.Column('date_approval', db.Date),
#     db.Column('status',db.String(40)),
#     db.Column('amount_sanctioned',db.String(40)),
#     db.Column('tenure',db.String(40)),
#     db.Column('feedback',db.String(400))
# )

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


loan_details = db.Table('loan_details',
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.employee_id')),
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.customer_id')),
    db.Column('loan_id',db.String(40), primary_key=True),
    db.Column('customer_name', db.String(50)),
    db.Column('email', db.String(60)),
    db.Column('loan_type',db.String(40)),
    db.Column('date_approval', db.Date),
    db.Column('status',db.String(40)),
    db.Column('amount_sanctioned',db.String(40)),
    db.Column('tenure',db.String(40)),
    db.Column('feedback',db.String(400))
)



class customer(db.Model, UserMixin):
    # userid = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer,primary_key=True)
    customer_name=db.Column(db.String(20))
    phone= db.Column(db.String(20))
    email = db.Column(db.String(40))
    password = db.Column(db.String(100))
    dob=db.Column(db.Date)
    gender=db.Column(db.String(10))
    address=db.Column(db.String(400))
    occupation = db.Column(db.String(40))
    annual_income = db.Column(db.String(40))

    apply = db.relationship('ApplyLoan', backref='customer', lazy=True)
    loan = db.relationship('employee', secondary=loan_details, lazy='subquery',
                                backref=db.backref('customers', lazy=True))
    def get_id(self):
        return self.customer_id

    def __init__(self,customer_id, customer_name, phone, email, dob ,gender, address, occupation, annual_income):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.phone= phone
        self.email = email
        # self.password = ''
        self.dob = dob
        self.gender = gender
        self.address = address
        self.occupation = occupation
        self.annual_income = annual_income


    def __repr__(self):
        return f"customer('{self.customer_name}', '{self.phone}', '{self.email}', '{self.dob}', '{self.gender}', '{self.address}', '{self.occupation}', '{self.annual_income}')"


class employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(20))
    emp_phone = db.Column(db.String(20))
    emp_email = db.Column(db.String(50))
    designation=db.Column(db.String(20))
    def __init__(self,empid,name,phone,email,designation):
        self.employee_id = empid
        self.employee_name=name
        self.emp_phone=phone
        self.emp_email=email
        self.designation=designation


class loan_status(db.Model):
    statusid = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'),nullable=False)
    customer_name =  db.Column(db.String(40))
    email = db.Column(db.String(40))
    loan_id=db.Column(db.String(40), primary_key=True)
    loan_type=db.Column(db.String(40))
    date_approval = db.Column(db.Date)
    status = db.Column(db.String(40))
    amount_sanctioned= db.Column(db.String(40))
    tenure=db.Column(db.String(40))
    feedback=db.Column(db.String(400))
    def __init__(self,statusid,employee_id,customername,email,loanid,type,date_approval,status,amount,tenure,feedback):
        self.statusid = statusid
        self.employee_id=employee_id
        self.customer_name=customername
        self.email=email
        self.loan_id = loanid
        self.loan_type=type
        self.date_approval = date_approval
        self.status=status
        self.amount_sanctioned = amount
        self.tenure=tenure
        self.feedback=feedback


class ApplyLoan(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'),
                          nullable=False)
    employee_id = db.Column(db.Integer)
    customer_name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    loan_type = db.Column(db.String(20))
    amount_needed = db.Column(db.String(20))
    status=db.Column(db.String(20))
    PAN=db.Column(db.String(400))
    aadhar= db.Column(db.String(400))
    passport = db.Column(db.String(300))
    applied_date= db.Column(db.Date)
    def __init__(self,loanid,customerid,employee_id,customername,email,type,amount,status,pan,aadhar, passport, applydate):
        self.loan_id = loanid
        self.customer_id=customerid
        self.employee_id = employee_id
        self.customer_name=customername
        self.email=email
        self.loan_type=type
        self.amount_needed=amount
        self.status=status
        self.PAN=pan
        self.aadhar=aadhar
        self.passport = passport
        self.applied_date=applydate

# admin.add_view(ModelView(customer, db.session))
# admin.add_view(ModelView(employee, db.session))
# admin.add_view(ModelView(ApplyLoan, db.session))
# admin.add_view(ModelView(loan_status, db.session))
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Role, db.session))

