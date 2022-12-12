from flask import Flask
import json
from os import system

with open('peliculas.json', encoding='utf-8') as archivo_json:
    peliculas = json.load(archivo_json)

with open('usuarios.json', encoding='utf-8') as archivo2_json:
    usuarios = json.load(archivo2_json)


opcion = int(input("Ingrese un numero: "))

if opcion == 1:
    #Ultimas 10 peliculas modo publico
    system('cls')
    print("Estas son las ultimas 10 peliculas agregadas")
    print(" ")
    listapeliculas = []
    for i in peliculas[::-1]:
        if len(listapeliculas)<10:
            listapeliculas.append(i)
        else:
            continue
    print(listapeliculas)
    exit()

else:
    while (True):
            system('cls')
            print("Menu de registro")
            print("Escriba 'salir' para volver al menu")
            usuario = input("Ingrese su nombre de usuario: ")
            if usuario == "salir":
                break
            else:    
                for nombre in usuarios:
                    if usuario == nombre["usuario"]:
                        id_nombre = nombre["id"]
                        contraseña = input("Ingrese su contraseña: ")
                        for clave in usuarios:
                            if contraseña == clave["contraseña"]:
                                id_contraseña = clave["id"]
                                if id_nombre == id_contraseña:
                                    print("Logueo correcto siguiente funcion")
                                    input("presione enter para seguir ")
                    break
    app = Flask(__name__)
    if __name__ == "__main__":
        app.run(debug=True)


    #Devolver la lista de directores presentes en la plataforma
    @app.route("/alldirectores", methods=["GET"])
    def directores():
        listadirectores = []
        for pelicula in peliculas:
            listadirectores.append(pelicula["director"])
        return listadirectores

    #Devolver la lista de películas dirigidas por un director en particular
    @app.route("/directores/<director>")
    def di(director):
        director_peliculas = []
        for pelicula in peliculas:
            if director == pelicula["director"]:
                director_peliculas.append(pelicula["title"])
        return director_peliculas

    #Devolver la lista de géneros presentes en la plataforma
    def generos():
        system('cls')
        print("Estos son los generos de pelicula disponibles")
        print(" ")
        listageneros = []
        for pelicula in peliculas:
            listageneros.append(pelicula["genero"])
        print(listageneros)
        print(" ")
        input("presione enter para seguir ")



    #Ultimas 10 peliculas modo publico
    def ultimas10(): 
        system('cls')
        print("Estas son las ultimas 10 peliculas agregadas")
        print(" ")
        listapeliculas = []
        for i in peliculas[::-1]:
            if len(listapeliculas)<10:
                listapeliculas.append(i)
            else:
                continue
        print(listapeliculas)
        print(" ")
        input("presione enter para seguir ")

    #Menu para usuarios ya registrados correctamente 
    def menu_registrado():
        while (True):
            system('cls')
            print('Que funcion desea realizar')
            print("1. Directores")
            print("2. Generos")
            print("3. Peliculas de un director")
            print("4. Peliculas con portada")
            print("5. Ver peliculas")
            print("6. Eliminar pelicula")
            print("7. Editar informacion de una pelicula")
            print("8. Agregar una pelicula")
            print("9. Salir")
            print(" ")
            funcion = int(input("Funcion: "))
                
            if (funcion == 1):
                directores()
                
            elif (funcion == 2):
                generos()

            elif (funcion == 3):
                director_peliculas()  

            elif (funcion == 9):
                break
                
            else:
                print('ERROR. Opcion invalida')
                input("Presiona enter para continuar")


    # #Verificacion de registro de usuario
    # def registro():
    #     while (True):
    #         system('cls')
    #         print("Menu de registro")
    #         print("Escriba 'salir' para volver al menu")
    #         usuario = input("Ingrese su nombre de usuario: ")
    #         if usuario == "salir":
    #             break
    #         else:    
    #             for nombre in usuarios:
    #                 if usuario == nombre["usuario"]:
    #                     id_nombre = nombre["id"]
    #                     contraseña = input("Ingrese su contraseña: ")
    #                     for clave in usuarios:
    #                         if contraseña == clave["contraseña"]:
    #                             id_contraseña = clave["id"]
    #                             if id_nombre == id_contraseña:
    #                                 print("Logueo correcto siguiente funcion")
    #                                 input("presione enter para seguir ")
    #                                 menu_registrado()

    #Menu inicial

        # print('MENU DE OPCIONES')
        # print("1. Ingresar en modo publico")
        # print("2. Ingresar con mi cuenta")
        # print("3. Salir")
        # opcion = int(input("Opcion: "))
        
        # if (opcion == 1):
        #     ultimas10() 
        
        # elif (opcion == 2):
        #     registro()
                
        # elif (opcion == 3):
        #     exit()
            
        # else:
        #     print('ERROR. Opcion invalida')
        #     input("Presiona enter para continuar")
