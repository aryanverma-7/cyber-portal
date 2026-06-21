from datetime import datetime
from models import db

class PhishingCase(db.Model):
    __tablename__ = 'phishing_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email_content = db.Column(db.Text, nullable=True)
    email_sender = db.Column(db.String(200), nullable=True)
    email_subject = db.Column(db.String(255), nullable=True)
    url_detected = db.Column(db.String(500), nullable=True)
    is_phishing = db.Column(db.Boolean, nullable=False)
    risk_score = db.Column(db.Float, nullable=False)  # 0-100
    detection_reasons = db.Column(db.Text, nullable=True)  # JSON string
    user_triggered = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_risk_level(self):
        if self.risk_score >= 80:
            return 'Critical'
        elif self.risk_score >= 60:
            return 'High'
        elif self.risk_score >= 40:
            return 'Medium'
        elif self.risk_score >= 20:
            return 'Low'
        return 'Safe'
    
    def get_reasons_list(self):
        if self.detection_reasons:
            import json
            try:
                return json.loads(self.detection_reasons)
            except:
                return [self.detection_reasons]
        return []