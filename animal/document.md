# README

動物病院の「飼い主・ペット・獣医・予約」を最小構成で管理する Flask アプリのスターターパックです。

- ローカル開発: SQLite（簡単に動く）
- 本番: MySQL（AWS RDS もしくは EC2 上の MySQL）
- ORM: SQLAlchemy（FK 整合性でハマりにくい）
- マイグレーション: Flask-Migrate
- 画面: Jinja2（シンプルな CRUD と予約登録フォーム）

---

## 1) ディレクトリ構成
```
vet_reservation/
├─ app.py
├─ config.py
├─ models.py
├─ routes/
│  ├─ __init__.py
│  ├─ owners.py
│  ├─ pets.py
│  ├─ vets.py
│  └─ appointments.py
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ owners/
│  │  ├─ list.html
│  │  └─ create.html
│  ├─ pets/
│  │  ├─ list.html
│  │  └─ create.html
│  ├─ vets/
│  │  ├─ list.html
│  │  └─ create.html
│  └─ appointments/
│     ├─ list.html
│     └─ create.html
├─ static/
│  └─ style.css
├─ .env.example
├─ requirements.txt
└─ wsgi.py
```

---

## 2) セットアップ
### 2.1 仮想環境 & 依存
```
python -m venv .venv
source .venv/bin/activate  # Windows は .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
```

### 2.2 .env（例）
```
# ローカルは SQLite で OK（ファイル一発）
FLASK_ENV=development
SECRET_KEY=dev-secret
SQLALCHEMY_DATABASE_URI=sqlite:///dev.db

# 本番例（MySQL/RDS）
# SQLALCHEMY_DATABASE_URI=mysql+pymysql://<user>:<pass>@<host>:3306/<db>?charset=utf8mb4
```

### 2.3 DB 初期化
```
flask db init
flask db migrate -m "init"
flask db upgrade
```

### 2.4 実行
```
flask run
# ブラウザ: http://127.0.0.1:5000
```

---

## 3) requirements.txt
```
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.7
python-dotenv==1.0.1
PyMySQL==1.1.1
```

---

## 4) config.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

## 5) models.py
```python
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
```

---

## 6) app.py
```python
from flask import Flask, render_template
from flask_migrate import Migrate
from models import get_db
from config import Config
from routes.owners import owners_bp
from routes.pets import pets_bp
from routes.vets import vets_bp
from routes.appointments import appointments_bp

_db = get_db()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    _db.init_app(app)
    Migrate(app, _db)

    # Blueprint 登録
    app.register_blueprint(owners_bp, url_prefix="/owners")
    app.register_blueprint(pets_bp, url_prefix="/pets")
    app.register_blueprint(vets_bp, url_prefix="/vets")
    app.register_blueprint(appointments_bp, url_prefix="/appointments")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

app = create_app()
```

---

## 7) routes/__init__.py
```python
# 空でOK（Blueprint 用）
```

---

## 8) routes/owners.py
```python
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
```

---

## 9) routes/pets.py
```python
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
```

---

## 10) routes/vets.py
```python
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
```

---

## 11) routes/appointments.py
```python
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
```

---

## 12) templates/base.html
```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>動物病院予約</title>
    <link rel="stylesheet" href="/static/style.css">
  </head>
  <body>
    <header>
      <h1>🏥 動物病院予約システム</h1>
      <nav>
        <a href="/">Home</a>
        <a href="/owners/">飼い主</a>
        <a href="/pets/">ペット</a>
        <a href="/vets/">獣医</a>
        <a href="/appointments/">予約</a>
      </nav>
      <hr>
    </header>
    <main>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <ul class="flash">
            {% for category, message in messages %}
              <li class="{{ category }}">{{ message }}</li>
            {% endfor %}
          </ul>
        {% endif %}
      {% endwith %}
      {% block content %}{% endblock %}
    </main>
  </body>
</html>
```

---

## 13) templates/index.html
```html
{% extends 'base.html' %}
{% block content %}
<h2>ようこそ！</h2>
<p>左のメニューからデータ登録＆予約を作成できます。</p>
{% endblock %}
```

---

## 14) owners 画面
### list.html
```html
{% extends 'base.html' %}
{% block content %}
<h2>飼い主一覧</h2>
<p><a href="/owners/create">＋ 新規登録</a></p>
<table>
  <tr><th>ID</th><th>名前</th><th>電話</th><th>Email</th><th>住所</th></tr>
  {% for o in owners %}
    <tr>
      <td>{{ o.id }}</td>
      <td>{{ o.name }}</td>
      <td>{{ o.phone }}</td>
      <td>{{ o.email }}</td>
      <td>{{ o.address }}</td>
    </tr>
  {% endfor %}
</table>
{% endblock %}
```

### create.html
```html
{% extends 'base.html' %}
{% block content %}
<h2>飼い主登録</h2>
<form method="post">
  <label>名前* <input name="name" required></label><br>
  <label>電話 <input name="phone"></label><br>
  <label>Email <input name="email" type="email"></label><br>
  <label>住所 <input name="address"></label><br>
  <button type="submit">保存</button>
</form>
{% endblock %}
```

---

## 15) pets 画面
### list.html
```html
{% extends 'base.html' %}
{% block content %}
<h2>ペット一覧</h2>
<p><a href="/pets/create">＋ 新規登録</a></p>
<table>
  <tr><th>ID</th><th>名前</th><th>種別</th><th>品種</th><th>飼い主</th></tr>
  {% for p in pets %}
    <tr>
      <td>{{ p.id }}</td>
      <td>{{ p.name }}</td>
      <td>{{ p.species }}</td>
      <td>{{ p.breed }}</td>
      <td>{{ p.owner.name }}</td>
    </tr>
  {% endfor %}
</table>
{% endblock %}
```

### create.html
```html
{% extends 'base.html' %}
{% block content %}
<h2>ペット登録</h2>
<form method="post">
  <label>名前* <input name="name" required></label><br>
  <label>種別* <input name="species" placeholder="dog/cat 等" required></label><br>
  <label>品種 <input name="breed"></label><br>
  <label>誕生日 <input name="birthdate" type="date"></label><br>
  <label>飼い主* 
    <select name="owner_id" required>
      {% for o in owners %}<option value="{{ o.id }}">{{ o.name }}</option>{% endfor %}
    </select>
  </label><br>
  <button type="submit">保存</button>
</form>
{% endblock %}
```

---

## 16) vets 画面
### list.html
```html
{% extends 'base.html' %}
{% block content %}
<h2>獣医一覧</h2>
<p><a href="/vets/create">＋ 新規登録</a></p>
<table>
  <tr><th>ID</th><th>名前</th><th>専門</th><th>電話</th></tr>
  {% for v in vets %}
    <tr>
      <td>{{ v.id }}</td>
      <td>{{ v.name }}</td>
      <td>{{ v.specialty }}</td>
      <td>{{ v.phone }}</td>
    </tr>
  {% endfor %}
</table>
{% endblock %}
```

### create.html
```html
{% extends 'base.html' %}
{% block content %}
<h2>獣医登録</h2>
<form method="post">
  <label>名前* <input name="name" required></label><br>
  <label>専門 <input name="specialty"></label><br>
  <label>電話 <input name="phone"></label><br>
  <button type="submit">保存</button>
</form>
{% endblock %}
```

---

## 17) appointments 画面
### list.html
```html
{% extends 'base.html' %}
{% block content %}
<h2>予約一覧</h2>
<p><a href="/appointments/create">＋ 新規作成</a></p>
<table>
  <tr><th>ID</th><th>日時</th><th>ペット</th><th>獣医</th><th>理由</th><th>状態</th></tr>
  {% for a in appointments %}
    <tr>
      <td>{{ a.id }}</td>
      <td>{{ a.start_at.strftime('%Y-%m-%d %H:%M') }}</td>
      <td>{{ a.pet.name }}</td>
      <td>{{ a.vet.name }}</td>
      <td>{{ a.reason }}</td>
      <td>{{ a.status }}</td>
    </tr>
  {% endfor %}
</table>
{% endblock %}
```

### create.html
```html
{% extends 'base.html' %}
{% block content %}
<h2>予約作成</h2>
<form method="post">
  <label>ペット* 
    <select name="pet_id" required>
      {% for p in pets %}<option value="{{ p.id }}">{{ p.name }}（{{ p.owner.name }}）</option>{% endfor %}
    </select>
  </label><br>
  <label>獣医* 
    <select name="vet_id" required>
      {% for v in vets %}<option value="{{ v.id }}">{{ v.name }}</option>{% endfor %}
    </select>
  </label><br>
  <label>日時* <input name="start_at" placeholder="2025-10-08 14:30" required></label><br>
  <label>理由 <input name="reason"></label><br>
  <button type="submit">保存</button>
</form>
{% endblock %}
```

---

## 18) static/style.css（最低限）
```css
body { font-family: system-ui, -apple-system, sans-serif; padding: 16px; }
nav a { margin-right: 12px; }
.flash { list-style: none; padding: 0; }
.flash li { padding: 8px; margin: 6px 0; border-radius: 6px; }
.flash .success { background: #eaffea; }
.flash .error { background: #ffecec; }
 table { border-collapse: collapse; width: 100%; }
 th, td { border: 1px solid #ddd; padding: 8px; }
 th { background: #f7f7f7; }
```

---

## 19) wsgi.py（デプロイ用）
```python
from app import app as application
```

---

## 20) AWS EC2（超シンプル手順）
1. EC2（Amazon Linux または Ubuntu）作成 → セキュリティグループで 80/22（必要なら 443）を開放。
2. Python3 & venv を入れる → プロジェクトを `git clone`。
3. `.env` を MySQL の接続文字列に差し替え。
4. `pip install -r requirements.txt`
5. `flask db upgrade` でスキーマ作成。
6. 本番サーバ: `gunicorn -w 2 -b 0.0.0.0:8000 wsgi:application`。
7. Nginx をリバースプロキシに設定（/ → 127.0.0.1:8000）。

---

## 21) サンプル初期データ（任意）
```sql
-- vets（獣医）
INSERT INTO vets (name, specialty, phone) VALUES
('田中先生', '内科', '03-1234-5678'),
('鈴木先生', '外科', '03-9876-5432');

-- owners（飼い主）
INSERT INTO owners (name, phone, email, address) VALUES
('佐藤太郎', '090-1111-2222', 'taro@example.com', '東京都千代田区'),
('山田花子', '090-3333-4444', 'hanako@example.com', '東京都港区');
```

---

## 22) よくあるつまずき対策
- **FK エラー**: 先に親（owners, vets）→子（pets）→孫（appointments）の順に登録。
- **日時フォーマット**: `YYYY-MM-DD HH:MM` 固定。バリデーション済。
- **MySQL 文字化け**: 接続文字列に `?charset=utf8mb4` を付ける。
- **タイムゾーン**: DB の `time_zone` を `+09:00`、アプリは JST 表示に統一。

---

## 23) 次ステップ（2〜3時間でできる）
- 予約の **重複チェック**（同一 vet で同時刻重複を禁止）
- 予約の **状態更新**（completed/cancelled への変更ボタン）
- **検索フィルタ**（日付/獣医/飼い主）
- **ログイン**（Flask-Login）と権限（受付/獣医）

---

> まずはローカルで `flask run` が通れば OK。MySQL への切替と EC2 配置は `.env` と `gunicorn + nginx` を追加するだけで行けます。
