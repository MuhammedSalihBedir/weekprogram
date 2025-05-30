from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# from sqlalchemy import Column, Integer, String, ForeignKey, and_
# from sqlalchemy.orm import foreign, relationship

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
    role = db.relationship('Role')

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

class TimeProfessor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    hour_id = db.Column(db.Integer, db.ForeignKey('hour.id'), nullable=False)
    
    professor = db.relationship('Person')
    day = db.relationship('Day')
    hour = db.relationship('Hour')

class LectureProfessor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)

    professor = db.relationship('Person')
    lecture = db.relationship('Lecture')

class LectureStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    lecture_professor_id = db.Column(db.Integer, db.ForeignKey('lecture_professor.id'), nullable=False)

    student = db.relationship('Person')
    lecture_professor = db.relationship('LectureProfessor')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    person_number = db.Column(db.String, db.ForeignKey('person.number'), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    person = db.relationship('Person')

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class LectureClassroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)

    classroom = db.relationship('Classroom')
    lecture = db.relationship('Lecture')

class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True, nullable=False)

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

class Hour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True, nullable=False)
    is_rest = db.Column(db.Boolean, nullable=False)


def seed_data(app, bcrypt):
    with app.app_context():
        if not Role.query.first():
            roles = [
                ("Admin"),
                ("Professor"),
                ("Student"),
            ]
            db.session.add_all(map(
                lambda x: Role(
                    name=x
                ),
                roles
            ))

        if not Person.query.first():
            people = [
                ("S001", "Hülya Kaya", 3),
                ("S002", "Hülya Çelik", 3),
                ("S003", "Ayşe Acar", 3),
                ("S004", "Fatma Eren", 3),

                ("P001", "Dr. Öğr. Üyesi Rasim ÇEKİK", 2),
                ("P002", "Dr. Öğr. Üyesi Adnan KOK", 2),
                ("P003", "Öğretm Görevls Metn ÇALMAN", 2),
                ("P004", "Dr. Öğr. Üyesi Dilan ALP", 2),
                ("P005", "Dr. Öğr. Üyesi Mustafa MIZRAK", 2),
                ("P006", "Doç. Dr. Bilal ALTAN", 2),
                ("P007", "Dr. Öğr. Üyesi Mehmet GÜL", 2),
                ("P008", "Doç. Dr. Mahmut DİRİK", 2),
                ("P009", "Dr. Öğr. Üyesi Kenan DONUK", 2),
                ("P010", "Dr. Öğr. Üyesi Emrullah GAZİOĞLU", 2),
                ("P011", "Doç. Dr. Murat ASLAN", 2),
                ("P012", "Doç. Dr. Asaf T. ÜLGEN", 2),

                ("A001", "Doç. Dr. Mahmut DİRİK", 1),
                ("A002", "Dr. Öğr. Üyesi Emrullah GAZİOĞLU", 1),
            ]
            db.session.add_all(map(
                lambda x: Person(
                    number=x[0],
                    name=x[1],
                    role_id=x[2]
                ),
                people
            ))

        if not User.query.first():
            users = [
                ("S001", "Hülya Kaya", 3),
                ("S002", "Hülya Çelik", 3),
                ("S003", "Ayşe Acar", 3),
                ("S004", "Fatma Eren", 3),

                ("P001", "Dr. Öğr. Üyesi Rasim ÇEKİK", 2),
                ("P002", "Dr. Öğr. Üyesi Adnan KOK", 2),
                ("P003", "Öğretm Görevls Metn ÇALMAN", 2),
                ("P004", "Dr. Öğr. Üyesi Dilan ALP", 2),
                ("P005", "Dr. Öğr. Üyesi Mustafa MIZRAK", 2),
                ("P006", "Doç. Dr. Bilal ALTAN", 2),
                ("P007", "Dr. Öğr. Üyesi Mehmet GÜL", 2),
                ("P008", "Doç. Dr. Mahmut DİRİK", 2),
                ("P009", "Dr. Öğr. Üyesi Kenan DONUK", 2),
                ("P010", "Dr. Öğr. Üyesi Emrullah GAZİOĞLU", 2),
                ("P011", "Doç. Dr. Murat ASLAN", 2),
                ("P012", "Doç. Dr. Asaf T. ÜLGEN", 2),

                ("A001", "Doç. Dr. Mahmut DİRİK", 1),
                ("A002", "Dr. Öğr. Üyesi Emrullah GAZİOĞLU", 1),
            ]
            db.session.add_all(map(
                lambda x: User(
                    person_number=x[0],
                    password=bcrypt.generate_password_hash("123"),
                ),
                users
            ))

        if not Lecture.query.first():
            lectures = [
                ("L001", "Mühendislk Etğ", 2, 1),
                ("L002", "Algoritma ve Programlama II", 5, 1),
                ("L003", "Makine Öğrenmesi", 3, 2),
                ("L004", "Türk Dili II", 2, 1),
                ("L005", "İngilizce II", 2, 1),
                ("L006", "Fizik II", 4, 1),
                ("L007", "Matematik II", 4, 1),
                ("L008", "Dfferansyel Denklemler", 4, 2),
                ("L009", "Olasılık ve İstatstk", 3, 2),
                ("L010", "Atatürk İlke ve İnkılapları", 2, 2),
                ("L011", "Nesne Tabanlı Programlama", 4, 2),
                ("L012", "İnsan Blgsayar Etkleşm", 2, 2),
                ("L013", "Görsel Programlama Dilleri", 4, 2),
                ("L014", "Mobil Tabanlı Uygulamalar", 2, 3),
                ("L015", "Gömülü Sistemi Programlama", 3, 4),
                ("L016", "Algoritmalar", 3, 2),
                ("L017", "Yapay Zeka", 3, 2),
                ("L018", "Bilişim Hukuku", 2, 2),
                ("L019", "Veri Madenciliğine Giriş", 3, 3),
                ("L020", "Yazılım Mühendislği", 4, 3),
                ("L021", "Bulanık Mantığın Temelleri", 4, 4),
                ("L022", "Bilgisayar Organizasyonu ve Mimarisi", 4, 2),
                ("L023", "Bilgisayar Mühendisliği Uygulamaları", 4, 3),
                ("L024", "Biçimsel Diller ve Otomata Teorisi", 3, 3),
                ("L025", "Algoritma Analizi", 3, 4),
                ("L026", "Veritabanı II", 3, 3),
                ("L027", "Bilgisayar Ağları", 3, 3),
                ("L028", "Optimizasyona Giriş", 3, 4),
                ("L029", "Elektrik Devreleri", 3, 1),
                ("L030", "Temel Bilgi Teknolojiler", 2, 1),
                ("L031", "Mikroişlemciler", 5, 2),
            ]
            db.session.add_all(map(
                lambda x: Lecture(
                    code=x[0],
                    name=x[1],
                    hours=x[2],
                    year=x[3]
                ),
                lectures
            ))

        if not LectureProfessor.query.first():
            lecture_professors = [
                (1+4, 1), # 1
                (1+4, 2), # 2
                (1+4, 3), # 3
                (2+4, 4), # 4
                (3+4, 5), # 5
                (4+4, 6), # 6
                (5+4, 7), # 7
                (5+4, 8), # 8
                (5+4, 9), # 9
                (6+4, 10), # 10
                (7+4, 11), # 11
                (7+4, 12), # 12
                (7+4, 13), # 13
                (7+4, 14), # 14
                (7+4, 15), # 15
                (8+4, 16), # 16
                (8+4, 17), # 17
                (9+4, 18), # 18
                (9+4, 19), # 19
                (9+4, 20), # 20
                (9+4, 21), # 21
                (10+4, 22), # 22
                (10+4, 23), # 23
                (10+4, 24), # 24
                (10+4, 25), # 25
                (11+4, 26), # 26
                (11+4, 27), # 27
                (11+4, 28), # 28
                (12+4, 29), # 29
                (11+4, 30), # 30
                (10+4, 31), # 31
            ]
            db.session.add_all(map(
                lambda x: LectureProfessor(
                    professor_id=x[0],
                    lecture_id=x[1]
                ),
                lecture_professors
            ))

        if not LectureStudent.query.first():
            lecture_students = [
                (1, 1),
                (1, 2),
                (1, 4),
                (1, 5),
                (1, 6),
                (1, 7),
                (1, 29),
                (2, 30),
                (2, 3),
                (2, 8),
                (2, 9),
                (2, 10),
                (2, 11),
                (3, 12),
                (3, 13),
                (3, 16),
                (2, 17),
                (3, 18),
                (2, 22),
                (3, 31),
                (3, 14),
                (3, 19),
                (3, 20),
                (3, 23),
                (3, 24),
                (3, 26),
                (3, 27),
                (4, 15),
                (4, 21),
                (4, 25),
                (4, 28),
            ]
            db.session.add_all(map(
                lambda x: LectureStudent(
                    student_id=x[0],
                    lecture_professor_id=x[1],
                ),
                lecture_students
            ))
        
        if not Year.query.first():
            years = [
                (1),
                (2),
                (3),
                (4),
            ]
            db.session.add_all(map(
                lambda x: Year(
                    name=x
                ),
                years
            ))
        
        if not Day.query.first():
            days = [
                ("Monday"),
                ("Tuesday"),
                ("Wednesday"),
                ("Thursday"),
                ("Friday"),
            ]
            db.session.add_all(map(
                lambda x: Day(
                    name=x
                ),
                days
            ))
        
        if not Hour.query.first():
            hours = [
                (8, False),
                (9, False),
                (10, False),
                (11, False),
                (12, True),
                (13, False),
                (14, False),
                (15, False),
                (16, False),
                (17, False),
            ]
            db.session.add_all(map(
                lambda x: Hour(
                    name=x[0],
                    is_rest=x[1]
                ),
                hours
            ))

        if not TimeProfessor.query.first():
            hour_ids = [
                1, 2, 3, 4, 6, 7, 8, 9, 10
            ]

            day_ids = [
                1, 2, 3, 4, 5,
            ]

            # Insert dummy professor schedule
            time_professors = [
                (person.id, d, h)
                for person in Person.query.filter_by(role_id=2).all()
                for h in hour_ids
                for d in day_ids
            ]
            db.session.add_all(map(
                lambda x: TimeProfessor(
                    professor_id=x[0],
                    day_id=x[1],
                    hour_id=x[2],
                ),
                time_professors
            ))
        
        if not Classroom.query.first():
            classrooms = [
                ("Lab 1", 10),
                ("Classroom 1", 10),
                ("Classroom 2", 10),
                ("Classroom 3", 10),
                ("Classroom 4", 10),
                ("Classroom 5", 10),
                ("Classroom 6", 10),
                ("Classroom 7", 10),
            ]
            db.session.add_all(map(
                lambda x: Classroom(
                    name=x[0],
                    capacity=x[1]
                ),
                classrooms
            ))
        
        if not LectureClassroom.query.first():
            lecture_classrooms = [
                (2, 1),
                (3, 1),
                (4, 1),
                (5, 1),
                (6, 1),
                (7, 1),
                (8, 1),

                (2, 2),
                (3, 2),
                (4, 2),
                (5, 2),
                (6, 2),
                (7, 2),
                (8, 2),
                
                (2, 3),
                (3, 3),
                (4, 3),
                (5, 3),
                (6, 3),
                (7, 3),
                (8, 3),
                
                (2, 4),
                (3, 4),
                (4, 4),
                (5, 4),
                (6, 4),
                (7, 4),
                (8, 4),
                
                (2, 5),
                (3, 5),
                (4, 5),
                (5, 5),
                (6, 5),
                (7, 5),
                (8, 5),
                
                (2, 6),
                (3, 6),
                (4, 6),
                (5, 6),
                (6, 6),
                (7, 6),
                (8, 6),
                
                (2, 7),
                (3, 7),
                (4, 7),
                (5, 7),
                (6, 7),
                (7, 7),
                (8, 7),
                
                (2, 8),
                (3, 8),
                (4, 8),
                (5, 8),
                (6, 8),
                (7, 8),
                (8, 8),
                
                (2, 9),
                (3, 9),
                (4, 9),
                (5, 9),
                (6, 9),
                (7, 9),
                (8, 9),
                
                (2, 10),
                (3, 10),
                (4, 10),
                (5, 10),
                (6, 10),
                (7, 10),
                (8, 10),
                
                (1, 11),
                
                (2, 12),
                (3, 12),
                (4, 12),
                (5, 12),
                (6, 12),
                (7, 12),
                (8, 12),
                
                (1, 13),
                
                (1, 14),
                
                (2, 15),
                (3, 15),
                (4, 15),
                (5, 15),
                (6, 15),
                (7, 15),
                (8, 15),
                
                (2, 16),
                (3, 16),
                (4, 16),
                (5, 16),
                (6, 16),
                (7, 16),
                (8, 16),
                
                (1, 17),
                
                (2, 18),
                (3, 18),
                (4, 18),
                (5, 18),
                (6, 18),
                (7, 18),
                (8, 18),
                
                (1, 19),
                
                (2, 20),
                (3, 20),
                (4, 20),
                (5, 20),
                (6, 20),
                (7, 20),
                (8, 20),
                
                (2, 21),
                (3, 21),
                (4, 21),
                (5, 21),
                (6, 21),
                (7, 21),
                (8, 21),
                
                (2, 22),
                (3, 22),
                (4, 22),
                (5, 22),
                (6, 22),
                (7, 22),
                (8, 22),
                
                (1, 23),
                
                (2, 24),
                (3, 24),
                (4, 24),
                (5, 24),
                (6, 24),
                (7, 24),
                (8, 24),
                
                (2, 25),
                (3, 25),
                (4, 25),
                (5, 25),
                (6, 25),
                (7, 25),
                (8, 25),
                
                (1, 26),
                
                (1, 27),
                
                (2, 28),
                (3, 28),
                (4, 28),
                (5, 28),
                (6, 28),
                (7, 28),
                (8, 28),
                
                (2, 29),
                (3, 29),
                (4, 29),
                (5, 29),
                (6, 29),
                (7, 29),
                (8, 29),
                
                (2, 30),
                (3, 30),
                (4, 30),
                (5, 30),
                (6, 30),
                (7, 30),
                (8, 30),
                
                (1, 31),
            ]
            db.session.add_all(map(
                lambda x: LectureClassroom(
                    classroom_id=x[0],
                    lecture_id=x[1]
                ),
                lecture_classrooms
            ))

        db.session.commit()

if __name__ == "__main__":
    from flask import Flask
    from config import Config
    from flask_bcrypt import Bcrypt

    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt = Bcrypt(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_data(app, bcrypt)