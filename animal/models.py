from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


# グローバル DB インスタンス
_db = SQLAlchemy()

def get_db():
    return _db

# ====== モデル ======
# 飼い主
class Owner(_db.Model):
    __tablename__ = "owners"
    id = _db.Column(_db.Integer, primary_key=True)
    name = _db.Column(_db.String(100), nullable=False)
    phone = _db.Column(_db.String(30), nullable=True)
    email = _db.Column(_db.String(120), nullable=True)
    address = _db.Column(_db.String(255), nullable=True)
    pets = _db.relationship("Pet", backref="owner", cascade="all, delete-orphan")

# ペット（患者）
class Pet(_db.Model):
    __tablename__ = "pets"
    id = _db.Column(_db.Integer, primary_key=True)
    name = _db.Column(_db.String(100), nullable=False)
    species = _db.Column(_db.String(50), nullable=False)  # dog/cat/etc
    breed = _db.Column(_db.String(100), nullable=True)
    birthdate = _db.Column(_db.Date, nullable=True)
    owner_id = _db.Column(_db.Integer, _db.ForeignKey("owners.id", ondelete="CASCADE"), nullable=False)
    appointments = _db.relationship("Appointment", backref="pet", cascade="all, delete-orphan")

# 獣医
class Vet(_db.Model):
    __tablename__ = "vets"
    id = _db.Column(_db.Integer, primary_key=True)
    name = _db.Column(_db.String(100), nullable=False)
    specialty = _db.Column(_db.String(100), nullable=True)
    phone = _db.Column(_db.String(30), nullable=True)
    appointments = _db.relationship("Appointment", backref="vet")

# 予約
class Appointment(_db.Model):
    __tablename__ = "appointments"
    id = _db.Column(_db.Integer, primary_key=True)
    pet_id = _db.Column(_db.Integer, _db.ForeignKey("pets.id", ondelete="CASCADE"), nullable=False)
    vet_id = _db.Column(_db.Integer, _db.ForeignKey("vets.id"), nullable=False)
    start_at = _db.Column(_db.DateTime, nullable=False)
    reason = _db.Column(_db.String(255), nullable=True)
    status = _db.Column(_db.String(20), nullable=False, default="scheduled")  # scheduled/completed/cancelled
    created_at = _db.Column(_db.DateTime, default=datetime.utcnow)
    updated_at = _db.Column(_db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        _db.CheckConstraint(status.in_(["scheduled", "completed", "cancelled"]), name="ck_appointment_status"),
    )
