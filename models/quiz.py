from datetime import datetime
from models import db

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # a, b, c, d
    difficulty = db.Column(db.String(20), nullable=False)  # easy, medium, hard
    category = db.Column(db.String(50), nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    points = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_options(self):
        return {
            'a': self.option_a,
            'b': self.option_b,
            'c': self.option_c,
            'd': self.option_d
        }
    
    def get_correct_answer(self):
        return self.get_options()[self.correct_option]


class QuizScore(db.Model):
    __tablename__ = 'quiz_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), nullable=False)
    selected_option = db.Column(db.String(1), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    points = db.Column(db.Integer, default=0)
    time_taken_seconds = db.Column(db.Integer, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    question = db.relationship('QuizQuestion', backref='scores')
    
    def calculate_points(self):
        self.points = self.question.points if self.is_correct else 0