from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import get_db, Pet, Owner

pets_bp = Blueprint("pets", __name__, template_folder="../templates/pets")
_db = get_db()

@pets_bp.get("/")
def list_pets():
    pets = Pet.query.order_by(Pet.id.desc()).all()
    return render_template("pets/list.html", pets=pets)

@pets_bp.get("/create")
def show_create():
    owners = Owner.query.order_by(Owner.name).all()
    return render_template("pets/create.html", owners=owners)

@pets_bp.post("/create")
def create_pet():
    name = request.form.get("name")
    species = request.form.get("species")
    breed = request.form.get("breed")
    birthdate = request.form.get("birthdate")
    owner_id = request.form.get("owner_id", type=int)

    if not name or not species or not owner_id:
        flash("必須項目が未入力です", "error")
        return redirect(url_for("pets.show_create"))

    pet = Pet(name=name, species=species, breed=breed or None, owner_id=owner_id)
    if birthdate:
        from datetime import date
        y,m,d = map(int, birthdate.split("-"))
        pet.birthdate = date(y,m,d)

    _db.session.add(pet)
    _db.session.commit()
    flash("ペットを登録しました", "success")
    return redirect(url_for("pets.list_pets"))
