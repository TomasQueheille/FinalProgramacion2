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
# Esta ruta esta creada con el fin de poder ingresar en modo publico en el caso de no contar con una cuenta, 
# esta ruta nos mostrara una lista con las ultimas 10 peliculas.
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
# La ruta Log fue creada con el fin de poder loguearse con un respectivo usuario y contraseña precargado para de esta forma poder 
# realizar diferentes funciones que no se encuentran en el modo publico.
# Modo de uso: Debemos escribir en el link /usuarios, luego abriremos otro slash en el cual ingresaremos un usuario para 
# posterior a ello colocar otro slash en el que introduciremos su respectiva contraseña la cual debe coincidir con el nombre de usuario.
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
        return jsonify({"OK": "Usted fue logueado con exito"}), HTTPStatus.OK
    else:
        return jsonify({"ERROR": "Usuario y/o Contraseña incorrectos"}), HTTPStatus.BAD_REQUEST                                          



#Devolver la lista de directores presentes en la plataforma
# La ruta alldirectores tiene el fin de devolver una lista con todos los directores cargados en la pagina.
@app.route("/alldirectores", methods=["GET"])   
def alldirectores():
    if modo == True:
        listadirectores = []
        for pelicula in peliculas:
            listadirectores.append(pelicula["director"])
        return listadirectores
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.FORBIDDEN  



#Devolver la lista de películas dirigidas por un director en particular
# La ruta directores se usa con el fin de encontrar las peliculas de un cierto director, debemos ingresar al lado de nuestra ruta /directores 
# y luego abriremos otro slash en el que pasaremos el nombre de un director, en el caso de que ese director no se encuentre en la pagina se le presentara un error, 
# por el caso contrario como explicamos con anterioridad se vera una lista con todas las peliculas de ese director.
@app.route("/directores/<director>")
def directores(director):
    if modo == True:
        director_peliculas = []
        for pelicula in peliculas:
            if director == pelicula["director"]:
                director_peliculas.append(pelicula["title"])
        return director_peliculas
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.FORBIDDEN  



#Devolver la lista de géneros presentes en la plataforma
# Lista generos a travez de un metodo "GET" nos obtendra una lista con los generos de todas las peliculas presente, 
# su modo de uso es sencillo, simplemente luego de copiar el link de la ruta debemos escribir /generos.
@app.route("/generos", methods=["GET"])
def generos():
    if modo == True:
        listageneros = []
        for pelicula in peliculas:
            listageneros.append(pelicula["genero"])
        return listageneros
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.FORBIDDEN  



#Devolver las películas que tienen imagen de portada agregada
# Con la ruta conportada obtendremos todas las peliculas que cuenten con url el cual contiene una imagen con la portada de la pelicula, 
# para poder utilizarlo ingresaremos el link de la ruta y escribiremos /conportada.
@app.route("/conportada", methods=["GET"])
def conportada():
    if modo == True:
        lista_portada = []
        for pelicula in peliculas:
            if "imgURL" in pelicula:
                lista_portada.append(pelicula["title"])        
        return lista_portada
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.FORBIDDEN  



#Crear pelicula
# Con la ruta crear pelicula notamos que usamos un metodo llamado "POST", esto nos permitira crear una pelicula nueva utilizando obligatoriamente 
# todos los campos los cuales son: 'anio', 'director', 'genero', 'imgURL', 'sinopsis', 'title'. En el caso de que no se ingrese alguno de estos campos, 
# nos retornara un error en el cual nos dira que algun campo es erroneo o no fue ingresado. 
# Tambien contamos con la condicion en la cual si se quiere psotear una pelicula que ya se encuentra por medio 
# de un for que recorre todos los titulos si encuentra la coincidencia le enviara un error diciendole que la pelicula ya existe.
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
        return jsonify({"ERROR": "Esa pelicula ya esta creada"}), HTTPStatus.BAD_REQUEST
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.FORBIDDEN 


#Crear comentario
# Esta funcion tiene el simple fin de comentar una pelicula, su metodo de uso es sencillo ingresaremos, {"comentario":"nuestro comentario"} y en la barra donde ingresamos el link debemos escribir a su lado /comentar/id, 
# id sera el id de la respectiva pelicula que deseamos comentar, 
# en el caso de que el id no exista se le mostrara un error el cual le dira que el id es incorrecto.
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
        return jsonify({"ERROR": "No hay pelicula con ese ID"}), HTTPStatus.BAD_REQUEST
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.FORBIDDEN  


#Ver peliculas
# Esta ruta nos devolvera una lista con todas las peliculas actuales que se encuentran cargadas en la pagina, 
# para utilizarlo simplemente luego de pegar el link debemos ingresar /allpeliculas.
@app.route("/allpeliculas", methods=["GET"])
def allpeliculas():
    if modo == True:
        todas_peliculas = []
        for pelicula in peliculas:
            todas_peliculas.append(pelicula)
        return todas_peliculas
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.FORBIDDEN 



#Borrar pelicula
# En esta ruta utilizamos el metodo "DELETE" con el fin de borrar una pelicula, para esto luego de ingresar el link debemos escribir /delete/id, 
# id sera el respectivo id de la pelicula que queremos borrar, sin embargo esto cuenta con la condicion que solo se puede borrar si esta no cuenta con comentarios, 
# si la pelicula que escoge para que sea eliminada tiene comentarios se le mostrara un error al igual que si el id es incorrecto.
@app.route("/delete/<id>", methods=["GET", "DELETE"])
def borrarpeliculas(id):
    if modo == True:
        contador = 0
        for pelicula in peliculas:
            if pelicula["id"] == int(id):
                if len(pelicula["comentarios"]) != 0:
                    return jsonify({"ERROR": "No se logro borrar"}), HTTPStatus.BAD_REQUEST
                else:
                    peliculas.pop(contador)
                    return jsonify({"OK": "Se ha borrado la pelicula"}), HTTPStatus.OK
            contador += 1
    else:
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.FORBIDDEN  



#Editar pelicula
# La ruta editar tiene el fin de editar la informacion de una pelicula ya existente, para utilizarla debemos ingresar al lado del link /editar/id, 
# el id sera el id de la pelicula que queremos editar, a su vez debemos en el apartado de "raw" agregar todas las caracteristicas con su edicion, 
# estos campos son: 'anio', 'director', 'genero', 'imgURL', 'sinopsis', 'title'. 
# En el caso de que no se ingrese alguno de estos campos, nos retornara un error en el cual nos dira que falta informacion.
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
        return jsonify({"ERROR": "No estas logueado"}), HTTPStatus.FORBIDDEN  