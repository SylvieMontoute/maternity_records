from flask import Flask, render_template, request
from sqlalchemy import create_engine
import settings
from models import Base, users # users, maternity, pregnancy
from utils import insert_data
from flask_simple_crypt import SimpleCrypt #for encryption

def create_app()->Flask:
    app = Flask(__name__)
    app.secret_key = settings.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{settings.dbuser}:{settings.dbpassword}@{settings.dbhost}/{settings.dbname}'
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    #Base.metadata.create_all(engine, checkfirst=True)
    return app

app = create_app()
cipher = SimpleCrypt()
cipher.init_app(app)

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method=='POST':
        result = request.form
        email = result['email']
        role = result['role']
        enc_email = cipher.encrypt(email)
        insert_data(create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True),table=users.User,email=enc_email, password="",role=role)
        return render_template('response.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)

"""

@app.route('/')
def welcome():
    return 'Welcome to Maternity Records!'
#def index():
    #return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method=='POST':
        result = request.form
        email = result['email']
        role = result['role']
        enc_email = cipher.encrypt(email)
        insert_data(create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True),table=users.User,email=enc_email, password="",role=role)
        return render_template('response.html', result=result)

if __name__ == '__main__':
    app.run(port =8080, debug=True)

    #instead use one line of code to create all of our tables
    
    # statement that creates all tables
   
    users.User.__table__.create(engine, checkfirst=True)
    maternity.Clients.__table__.create(engine, checkfirst=True)
    maternity.ClientReg.__table__.create(engine, checkfirst=True)
    pregnancy.PregnancyReg.__table__.create(engine, checkfirst=True)
    pregnancy.PregRiskAssessment.__table__.create(engine, checkfirst=True)
    pregnancy.PregFollowUp.__table__.create(engine, checkfirst=True)
    pregnancy.PregLabor.__table__.create(engine, checkfirst=True)
    pregnancy.PregPartograph.__table__.create(engine, checkfirst=True)
    pregnancy.PregPostPartum.__table__.create(engine, checkfirst=True)
    pregnancy.Death.__table__.create(engine, checkfirst=True)

    # insert into the tables
    insert_data(engine,users.User,email="test@test.com",password="password",role="CLIENT" )
    insert_data(engine,users.User,email="tes2t@test.com",password="password",role="CLINICAL" )"""   


