from flask import Flask, jsonify, Response, request
import json
from os import system
from http import HTTPStatus

app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)


with open('peliculas.json', encoding='utf-8') as archivo_json:
    peliculas = json.load(archivo_json)


with open('usuarios.json', encoding='utf-8') as archivo2_json:
    usuarios = json.load(archivo2_json)


modo = False #Si modo es false es publico, si es true es privado


#Ultimas 10 peliculas modo publico
@app.route("/nolog")
def nolog():    
    listapeliculas = []
    for i in peliculas[::-1]:
        if len(listapeliculas)<10:
            listapeliculas.append(i)
        else:
            continue
    return listapeliculas



#Modo logueado
@app.route("/usuarios/<usuario>/<contrasenia>", methods=["GET"])
def registro(usuario, contrasenia):
    global modo
    modo = False
    for nombre in usuarios:
        if usuario == nombre["usuario"]:
            id_nombre = nombre["id"]
            for clave in usuarios:
                if contrasenia == clave["contraseña"]:
                    id_contraseña = clave["id"]
                    if id_nombre == id_contraseña:
                        modo = True
    if modo == True:
        return Response(status=HTTPStatus.OK)
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.NO_CONTENT                                          



#Devolver la lista de directores presentes en la plataforma
@app.route("/alldirectores", methods=["GET"])   
def alldirectores():
    if modo == True:
        listadirectores = []
        for pelicula in peliculas:
            listadirectores.append(pelicula["director"])
        return listadirectores
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.NO_CONTENT  



#Devolver la lista de películas dirigidas por un director en particular
@app.route("/directores/<director>")
def directores(director):
    if modo == True:
        director_peliculas = []
        for pelicula in peliculas:
            if director == pelicula["director"]:
                director_peliculas.append(pelicula["title"])
        return director_peliculas
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.NO_CONTENT  



#Devolver la lista de géneros presentes en la plataforma
@app.route("/generos", methods=["GET"])
def generos():
    if modo == True:
        listageneros = []
        for pelicula in peliculas:
            listageneros.append(pelicula["genero"])
        return listageneros
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.NO_CONTENT  



#Devolver las películas que tienen imagen de portada agregada
@app.route("/conportada", methods=["GET"])
def conportada():
    if modo == True:
        lista_portada = []
        for pelicula in peliculas:
            if "imgURL" in pelicula:
                lista_portada.append(pelicula["title"])        
        return lista_portada
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.NO_CONTENT  



#Crear pelicula
@app.route("/crear", methods=["POST"])
def crear_pelicula():
    if modo == True:
        nuevapelicula = request.get_json()
        if 'anio' and 'director' and 'genero' and 'imgURL' and 'sinopsis' and 'title' not in nuevapelicula:
            return jsonify({"Error": "Campos erroneos o invalidos"}), HTTPStatus.BAD_REQUEST
        nuevoid = peliculas[-1]['id'] + 1
        titles = [t['title'] for t in peliculas]
        if nuevapelicula["title"] not in titles:
            pelicula = {
            "anio": nuevapelicula["anio"],
            "director": nuevapelicula["director"],
            "genero": nuevapelicula["genero"],
            "id": nuevoid,
            "imgURL": nuevapelicula["imgURL"],
            "sinopsis": nuevapelicula["sinopsis"],
            "title": nuevapelicula["title"],
            "comentarios": []
            }
            peliculas.append(pelicula)
            return pelicula, HTTPStatus.OK
        return jsonify({"Error": "Esa pelicula ya esta creada"}), HTTPStatus.BAD_REQUEST
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.NO_CONTENT 


#Crear comentario
@app.route("/comentar/<id>", methods=["POST"])
def comentar(id):
    if modo == True:
        nuevocomentario = request.get_json()
        for pelicula in peliculas:
            if pelicula["id"] == int(id):
                comentarios = pelicula["comentarios"]
                if not "comentario" in nuevocomentario:
                    return jsonify({"Error": "se espera un comentario"}), HTTPStatus.BAD_REQUEST
                else:
                    comentario = {
                        "comentario" : nuevocomentario["comentario"]
                    }
                    comentarios.append(comentario)
                    return jsonify({"OK":"Se ha creado el comentario"}), HTTPStatus.OK
        return jsonify({"Error": "No hay pelicula con ese ID"}), HTTPStatus.BAD_REQUEST
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.NO_CONTENT  


#Ver peliculas
@app.route("/allpeliculas", methods=["GET"])
def allpeliculas():
    if modo == True:
        todas_peliculas = []
        for pelicula in peliculas:
            todas_peliculas.append(pelicula)
        return todas_peliculas
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.NO_CONTENT 



#Borrar pelicula
@app.route("/delete/<id>", methods=["DELETE"])
def borrarpeliculas(id):
    if modo == True:
        contador = 0
        for pelicula in peliculas:
            if pelicula["id"] == int(id):
                if len(pelicula["comentarios"]) != 0:
                    return jsonify({"ERROR": "No se logro borrar"}), HTTPStatus.NO_CONTENT
                else:
                    peliculas.pop(contador)
                    return jsonify({"OK": "Se ha borrado la pelicula"}), HTTPStatus.OK
            contador += 1
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.NO_CONTENT  



#Editar pelicula
@app.route("/editar/<id>", methods=["PUT"])
def edicion(id):
    if modo == True:
        nuevosdatos = request.get_json()
        if not nuevosdatos:
            return jsonify({"ERROR": 'No hay datos a cambiar'}), HTTPStatus.BAD_REQUEST
        else:
            pos = int(id)   
            ids = [pelicula["id"] for pelicula in peliculas]
            if pos not in ids:
                return jsonify({"ERROR": "No hay peliculas con ese ID"}), HTTPStatus.NO_CONTENT
            if "anio" and "director" and "genero" and "imgURL" and "sinopsis" and "title" not in nuevosdatos:
                return jsonify({"ERROR": 'Falta informacion'}), HTTPStatus.BAD_REQUEST    
            else:
                for pelicula in peliculas:
                    if pelicula["id"] == int(id):
                        movie = peliculas[pos - 1]
                        comm = movie["comentarios"]
                        peliculas[pos - 1] = {
                        "title": nuevosdatos["title"],
                        "sinopsis": nuevosdatos["sinopsis"],
                        "director": nuevosdatos["director"],
                        "genero": nuevosdatos["genero"],
                        "anio": nuevosdatos["anio"],
                        "id": pos,
                        "imgURL": nuevosdatos["imgURL"],
                        "comentarios": comm
                        }
                        return jsonify({'mensaje':'good'}), HTTPStatus.OK
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.NO_CONTENT  