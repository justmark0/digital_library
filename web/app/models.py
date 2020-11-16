from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


raters = db.Table('raters',
                  db.Column('student_id', db.Integer, db.ForeignKey('student.student_id'), primary_key=True),
                  db.Column('material_id', db.Integer, db.ForeignKey('material.material_id'), primary_key=True)
                  )

professors = db.Table('professors',
                      db.Column('prof_id', db.Integer, db.ForeignKey('professor.prof_id'), primary_key=True),
                      db.Column('subject_id', db.Integer, db.ForeignKey('subject.subject_id'), primary_key=True)
                      )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password_hash = db.Column(db.String(512), nullable=False)
    is_student = db.relationship('Student', uselist=False, backref='user')  # one-to-one
    is_professor = db.relationship('Professor', uselist=False, backref='user')  # one-to_one
    is_moderator = db.relationship('Moderator', uselist=False, backref='user')  # one-to_one
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<{}:{}>'.format(self.id, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    suggests = db.relationship('Material', backref='author', lazy='dynamic')  # ont-to-many
    rated = db.relationship('Material', secondary=raters, backref=db.backref('raters', lazy='dynamic'))  # many-to-many

    def like(self, material):
        if material not in self.rated:
            self.rated.append(material)
            material.rating += 1

    def unlike(self, material):
        if material in self.rated:
            self.rated.remove(material)
            material.rating -= 1

    def dislike(self, material):
        if material not in self.rated:
            self.rated.append(material)
            material.rating -= 1

    def undislike(self, material):
        if material not in self.rated:
            self.rated.remove(material)
            material.rating += 1


class Professor(db.Model):
    prof_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    approved = db.relationship('Material', backref='author', lazy='dynamic')  # one-to-many
    rated = db.relationship('Subject', secondary=professors, backref=db.backref('professors', lazy='dynamic'))  # many-to-many


class Moderator(db.Model):
    mod_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


class Subject(db.Model):
    subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(512))


class Material(db.Model):
    material_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    suggested_by = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer, default=10)
    data = db.Column(db.LargeBinary)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<{}:{}:{}:{}>'.format(self.material_id, self.name, self.rating, self.data)
