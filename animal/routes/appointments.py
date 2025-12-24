from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import get_db, Appointment, Pet, Vet
from datetime import datetime

appointments_bp = Blueprint("appointments", __name__, template_folder="../templates/appointments")
_db = get_db()

@appointments_bp.get("/")
def list_appointments():
    # 最新順＋関連名表示のため JOIN 風味の取得
    appointments = (
        Appointment.query
        .order_by(Appointment.start_at.desc())
        .all()
    )
    return render_template("appointments/list.html", appointments=appointments)

@appointments_bp.get("/create")
def show_create():
    pets = Pet.query.order_by(Pet.name).all()
    vets = Vet.query.order_by(Vet.name).all()
    return render_template("appointments/create.html", pets=pets, vets=vets)

@appointments_bp.post("/create")
def create_appointment():
    pet_id = request.form.get("pet_id", type=int)
    vet_id = request.form.get("vet_id", type=int)
    start_at = request.form.get("start_at")  # '2025-10-08 14:30'
    reason = request.form.get("reason")

    if not pet_id or not vet_id or not start_at:
        flash("必須項目が未入力です", "error")
        return redirect(url_for("appointments.show_create"))

    try:
        dt = datetime.strptime(start_at, "%Y-%m-%d %H:%M")
    except ValueError:
        flash("日時は YYYY-MM-DD HH:MM 形式で入力してください", "error")
        return redirect(url_for("appointments.show_create"))

    ap = Appointment(pet_id=pet_id, vet_id=vet_id, start_at=dt, reason=reason or None)
    _db.session.add(ap)
    _db.session.commit()
    flash("予約を登録しました", "success")
    return redirect(url_for("appointments.list_appointments"))
