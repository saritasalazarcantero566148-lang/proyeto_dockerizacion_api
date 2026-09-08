from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "gestor_tareas")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Tarea(db.Model):
    __tablename__ = "tareas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)
    completada = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "completada": self.completada,
            "fecha_creacion": self.fecha_creacion.isoformat(),
        }


@app.route("/api/salud", methods=["GET"])
def salud():
    return jsonify({"estado": "ok"})

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/api/tareas", methods=["GET"])
def listar_tareas():
    tareas = Tarea.query.order_by(Tarea.id).all()
    return jsonify([t.to_dict() for t in tareas])


@app.route("/api/tareas/<int:tarea_id>", methods=["GET"])
def obtener_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    return jsonify(tarea.to_dict())


@app.route("/api/tareas", methods=["POST"])
def crear_tarea():
    datos = request.get_json(silent=True) or {}
    titulo = datos.get("titulo")

    if not titulo:
        return jsonify({"error": "El campo 'titulo' es obligatorio"}), 400

    tarea = Tarea(
        titulo=titulo,
        descripcion=datos.get("descripcion"),
        completada=datos.get("completada", False),
    )
    db.session.add(tarea)
    db.session.commit()
    return jsonify(tarea.to_dict()), 201


@app.route("/api/tareas/<int:tarea_id>", methods=["PUT"])
def actualizar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    datos = request.get_json(silent=True) or {}

    tarea.titulo = datos.get("titulo", tarea.titulo)
    tarea.descripcion = datos.get("descripcion", tarea.descripcion)
    tarea.completada = datos.get("completada", tarea.completada)

    db.session.commit()
    return jsonify(tarea.to_dict())


@app.route("/api/tareas/<int:tarea_id>", methods=["DELETE"])
def eliminar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    db.session.delete(tarea)
    db.session.commit()
    return jsonify({"mensaje": "Tarea eliminada"})


@app.cli.command("init-db")
def init_db():
    """Crea las tablas en la base de datos."""
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
