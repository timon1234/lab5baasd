from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fit.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)
app.app_context().push()

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=False)
    trainer = db.relationship("Trainer", back_populates="lessons")
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    hall = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<lessons {self.id}"

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    working_hours = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<branches {self.id}"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(1000), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<bookings {self.id}"

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<services {self.id}"

class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), nullable=False)
    lessons = db.relationship("Lesson", back_populates="trainer")

    def __repr__(self):
        return f"<trainers {self.id}"



@app.route("/")
def view_home():
    return render_template("index.html", title='Река-фит')

@app.route("/aboutus")
def view_aboutUs_page():
    trainers = Trainer.query.order_by(Trainer.id).all()
    branches = Branch.query.order_by(Branch.id).all()
    return render_template("aboutUs.html", trainers=trainers, branches=branches, title="О нас")


@app.route("/services")
def view_services_page():
    services = Service.query.all()
    return render_template("services.html", services=services, title="Услуги")

@app.route("/schedule")
def view_schedule_page():
    lessons = Lesson.query.order_by(Lesson.date, Lesson.start_time).all()

    schedule = defaultdict(lambda: defaultdict(list))
    for lesson in lessons:
        month = lesson.date.strftime('%B %Y')
        day = lesson.date.strftime('%Y-%m-%d')
        schedule[month][day].append(lesson)

    return render_template("schedule.html", title="Расписание", schedule=schedule)


@app.route("/sign_up", methods=['POST','GET'])
def view_sign_up_page():
    lessons = Lesson.query.order_by(Lesson.id).all()
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']
        activity = request.form['activity']
        lesson_id, date = activity.split(',')
        date = datetime.strptime(date.strip(), '%Y-%m-%d %H:%M:%S')

        book = Booking(name=name, surname=surname, phone_number=phone, lesson_id=lesson_id, date=date)

        try:
            db.session.add(book)
            db.session.commit()
            return redirect('/')
        except:
            return 'При записи произошла ошибка, попробуйте позже'
    else:
        return render_template("sign_up.html",lessons=lessons,title="Записаться")

@app.route("/contacts")
def view_contacts_page():
    return render_template("contacts.html", title="Контакты")


if __name__ == '__main__':
    app.run(debug=True)


    