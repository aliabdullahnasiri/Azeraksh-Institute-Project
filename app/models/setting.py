from app.extensions import db


class Setting(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), nullable=False)
    site_description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    primary_phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)

    # Social links
    facebook = db.Column(db.String(255), nullable=True)
    twitter = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(255), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)
    youtube = db.Column(db.String(255), nullable=True)

    # Optional extra fields
    logo_url = db.Column(db.String(255), nullable=True)
    favicon_url = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "site_name": self.site_name,
            "site_description": self.site_description,
            "location": self.location,
            "primary_phone": self.primary_phone,
            "email": self.email,
            "facebook": self.facebook,
            "twitter": self.twitter,
            "instagram": self.instagram,
            "linkedin": self.linkedin,
            "youtube": self.youtube,
            "logo_url": self.logo_url,
            "favicon_url": self.favicon_url,
        }
