from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import get_db, Vet

vets_bp = Blueprint("vets", __name__, template_folder="../templates/vets")
_db = get_db()

@vets_bp.get("/")
def list_vets():
    vets = Vet.query.order_by(Vet.id.desc()).all()
    return render_template("vets/list.html", vets=vets)

@vets_bp.get("/create")
def show_create():
    return render_template("vets/create.html")

@vets_bp.post("/create")
def create_vet():
    name = request.form.get("name")
    specialty = request.form.get("specialty")
    phone = request.form.get("phone")

    if not name:
        flash("名前は必須です", "error")
        return redirect(url_for("vets.show_create"))

    vet = Vet(name=name, specialty=specialty or None, phone=phone or None)
    _db.session.add(vet)
    _db.session.commit()
    flash("獣医を登録しました", "success")
    return redirect(url_for("vets.list_vets"))
