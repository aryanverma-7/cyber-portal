from app import app
from models.course import Course

with app.app_context():
    courses = Course.query.all()

    print("\nCOURSES FOUND:")
    print("=" * 50)

    for c in courses:
        print(c.id, c.title)

    print("=" * 50)
    print("TOTAL:", len(courses))