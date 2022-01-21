from flask import Flask, render_template
from flask_migrate import Migrate
from database import db
from forms import PersonForm
from models import Person

app = Flask(__name__)

# DataBase Configuration
USER_DB = 'postgres'
PASS_DB = 'root'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configure flasf-migrate
migrate = Migrate()
migrate.init_app(app, db)

# Configure flask-wtf
app.config['SECRET_KEY']='secret_key'

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    # People List
    people = Person.query.all()
    total_people = Person.query.count()
    app.logger.debug(f'People List: {people}')
    app.logger.debug(f'Total people: {total_people}')
    return render_template('index.html', people=people, total_people=total_people)

@app.route('/get_detail/<int:id>')
def get_detail(id):
    # Get person by id
    # person = Person.query.get(id)
    person = Person.query.get_or_404(id)
    app.logger.debug(f'Get person: {person}')
    return render_template('detail.html', person=person)

@app.route('/add', methods=['GET', 'POST'])
def add():
    person = Person()
    personForm = PersonForm(obj=person)
    return render_template('add.html', personForm=personForm)
