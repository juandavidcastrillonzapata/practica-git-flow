from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///juegos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class VideoJuego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "fecha": self.fecha
        }

with app.app_context():
    db.create_all()

@app.route("/videojuego/registrar", methods=["POST"])
def registrar():
    data = request.get_json()
    if data:
        videojuego = VideoJuego(
            titulo=data["titulo"], 
            descripcion=data["descripcion"], 
            precio=int(data["precio"]), 
            fecha=datetime.strptime(data["fecha"], "%Y-%m-%d")
        )
        db.session.add(videojuego)
        db.session.commit()
        return jsonify(videojuego.to_dict()), 201
    return jsonify({"error": "Falta campo"}), 400

@app.route("/videojuego/consultar", methods=["GET"])
def consultar():
        consulta = VideoJuego.query.all()
        return jsonify([juego.to_dict() for juego in consulta]), 200

@app.route("/videojuego/consultaprecio/<precio>", methods=["GET"])
def consultar_por_precio(precio):
    consulta = VideoJuego.query.filter_by(precio=int(precio)).all()
    return jsonify([juego.to_dict() for juego in consulta]), 200

@app.route("/videojuego/consultatitulo/<titulo>", methods=["GET"])
def consultar_por_titulo(tiulo):
    consulta = VideoJuego.query.filter_by(titulo=tiulo).all()
    return jsonify([juego.to_dict() for juego in consulta]), 200

@app.route("/videojuego/actualizar/<titulo>", methods=["PUT"])
def actualizar(titulo):
    actualizacion = request.get_json()
    if not actualizacion:
        return jsonify({"error": "Falta campo"}), 400
    consulta = VideoJuego.query.filter_by(titulo=titulo).first()
    if consulta:
        consulta.titulo = actualizacion["titulo"]
        consulta.descripcion = actualizacion["descripcion"]
        consulta.precio = actualizacion["precio"]
        consulta.fecha = datetime.strptime(actualizacion["fecha"], "%Y-%m-%d")
        db.session.commit()
        return jsonify(consulta.to_dict()), 200
    return jsonify({"error": "No existe el juego"}), 404

@app.route("/videojuego/eliminar/<titulo>", methods=["DELETE"])
def eliminar(titulo):
    consulta = VideoJuego.query.filter_by(titulo=titulo).first()
    if consulta:
        db.session.delete(consulta)
        db.session.commit()
        return jsonify({"titulo": titulo}), 200
    return jsonify({"error": "No existe el juego"}), 404

if __name__ == "__main__":
    app.run(debug=True)

#hola
#esta es mi api

#hola otra vez

# hola y chao 


