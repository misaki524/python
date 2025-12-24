from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import get_db, Owner

owners_bp = Blueprint("owners", __name__, template_folder="../templates/owners")
_db = get_db()

@owners_bp.get("/")
def list_owners():
    owners = Owner.query.order_by(Owner.id.desc()).all()
    return render_template("owners/list.html", owners=owners)

@owners_bp.get("/create")
def show_create():
    return render_template("owners/create.html")

@owners_bp.post("/create")
def create_owner():
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    address = request.form.get("address")

    if not name:
        flash("名前は必須です", "error")
        return redirect(url_for("owners.show_create"))

    owner = Owner(name=name, phone=phone, email=email, address=address)
    _db.session.add(owner)
    _db.session.commit()
    flash("飼い主を登録しました", "success")
    return redirect(url_for("owners.list_owners"))
