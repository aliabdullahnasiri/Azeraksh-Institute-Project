from app.extensions import db


class View(db.Model):
    __tablename__ = "views"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(255))
