from musical import db, ma


student_roles = db.Table(
    "student_roles",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)

song_performers = db.Table(
    "song_performers",
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)


class Production(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False) 
    subtitle = db.Column(db.String())
    cover_image = db.Column(db.String())
    location = db.Column(db.String())
    price = db.Column(db.String())
    copyright_info = db.Column(db.String())
    notes = db.Column(db.Text)

    crew = db.relationship("Crew", backref="production", lazy=True)
    team = db.relationship("Team", backref="production", lazy=True)
    dates = db.relationship("PerformanceDate", backref="production")
    songs = db.relationship("Song", backref="production")
    roles = db.relationship("Role", backref="production")
    thanks = db.relationship("Thanks", backref="production", lazy=True)  # <-- FIXED


class PerformanceDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    intermission_length = db.Column(db.String(50))
    production_id = db.Column(db.Integer, db.ForeignKey("production.id"), nullable=False)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sex = db.Column(db.String(10))
    year = db.Column(db.String(20)) 
    roles = db.relationship("Role", secondary=student_roles, back_populates="students")


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    actor = db.Column(db.String(120), nullable=False)
    is_group = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    production_id = db.Column(db.Integer, db.ForeignKey("production.id"), nullable=False)

    students = db.relationship("Student", secondary=student_roles, back_populates="roles")
    songs = db.relationship("Song", secondary=song_performers, back_populates="roles")


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    act_number = db.Column(db.Integer, default=1)
    is_reprise = db.Column(db.Boolean, default=False)
    who_sings = db.Column(db.String(), nullable=False)

    production_id = db.Column(db.Integer, db.ForeignKey("production.id"), nullable=False)
    roles = db.relationship("Role", secondary=song_performers, back_populates="songs")


class Thanks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    production_id = db.Column(db.Integer, db.ForeignKey("production.id"), nullable=False)
    thanks_text = db.Column(db.String(), nullable=True)

class Crew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    responsibility = db.Column(db.String(120))
    production_id = db.Column(db.Integer, db.ForeignKey("production.id"), nullable=False)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120))  # e.g. Director, Choreographer
    production_id = db.Column(db.Integer, db.ForeignKey("production.id"), nullable=False)



class CrewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Crew
        load_instance = True
class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        load_instance = True


class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True

class SongSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Song
        load_instance = True

class ProductionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Production
        load_instance = True

class ThanksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Thanks
        load_instance = True
