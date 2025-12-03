import csv
from musical import db
from musical.models import Student

def import_students_from_csv(filepath: str):
    """
    Import students from a CSV file into the database.
    CSV format: name,sex,year
    Example row: Michael Rogers,F,Junior
    """
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['name', 'sex', 'year'])
        for row in reader:
            name = row['name'].strip()
            sex = row['sex'].strip()
            year = row['year'].strip()

            existing = Student.query.filter_by(name=name, year=year).first()
            if not existing:
                student = Student(name=name, sex=sex, year=year)
                db.session.add(student)

        db.session.commit()

