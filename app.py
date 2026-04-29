import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# -----------------------
# Flask + configuración
# -----------------------
app = Flask(__name__)
load_dotenv()  # lee variables de .env

database_url = os.getenv('DATABASE_URL', 'postgresql://recetario_user:recetario_pass@db:5432/recetario')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------
# Modelo
# -----------------------
class Receta(db.Model):
    __tablename__ = 'recetas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(60))
    tiempo_min = db.Column(db.Integer)
    porciones = db.Column(db.Integer)
    ingredientes = db.Column(db.Text)
    instrucciones = db.Column(db.Text)

# -----------------------
# Crear tablas si no existen
# -----------------------
with app.app_context():
    db.create_all()

# -----------------------
# Evitar caché del navegador
# -----------------------
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store"
    return response

# -----------------------
# Rutas
# -----------------------
@app.route("/")
def home():
    recetas = Receta.query.order_by(Receta.id.desc()).all()
    return render_template("index.html", recetas=recetas)

@app.route("/recetas/nueva", methods=["GET", "POST"])
def nueva_receta():
    if request.method == "POST":
        receta = Receta(
            titulo=request.form["titulo"].strip(),
            categoria=request.form.get("categoria", "").strip(),
            tiempo_min=int(request.form.get("tiempo_min") or 0),
            porciones=int(request.form.get("porciones") or 0),
            ingredientes=request.form.get("ingredientes", "").strip(),
            instrucciones=request.form.get("instrucciones", "").strip(),
        )
        db.session.add(receta)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("nueva_receta.html")

@app.route("/recetas/<int:id>")
def ver_receta(id):
    receta = Receta.query.get_or_404(id)
    return render_template("ver_receta.html", receta=receta)

@app.route("/recetas/<int:id>/editar", methods=["GET", "POST"])
def editar_receta(id):
    receta = Receta.query.get_or_404(id)
    if request.method == "POST":
        receta.titulo = request.form["titulo"].strip()
        receta.categoria = request.form.get("categoria", "").strip()
        receta.tiempo_min = int(request.form.get("tiempo_min") or 0)
        receta.porciones = int(request.form.get("porciones") or 0)
        receta.ingredientes = request.form.get("ingredientes", "").strip()
        receta.instrucciones = request.form.get("instrucciones", "").strip()
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("editar_receta.html", receta=receta)

@app.route("/recetas/<int:id>/eliminar", methods=["POST"])
def eliminar_receta(id):
    receta = Receta.query.get_or_404(id)
    db.session.delete(receta)
    db.session.commit()
    return redirect(url_for("home"))

# -----------------------
# Run local / Docker
# -----------------------
if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5001, debug=True)