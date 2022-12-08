import json

with open('peliculas.json', encoding='utf-8') as archivo_json:
    peliculas = json.load(archivo_json)

#Devolver la lista de directores presentes en la plataforma
def directores():
    listadirectores = []
    for pelicula in peliculas:
        listadirectores.append(pelicula["director"])
    print(listadirectores)

#Devolver la lista de géneros presentes en la plataforma
def generos():
    listageneros = []
    for pelicula in peliculas:
        listageneros.append(pelicula["genero"])
    print(listageneros)

#Ultimas 10 peliculas modo publico
def ultimas10(): 
    listapeliculas = []
    for i in peliculas[::-1]:
        if len(listapeliculas)<10:
            listapeliculas.append(i)
        else:
            continue
    print(listapeliculas)

while (True):
    print('MENU DE OPCIONES')
    print("1. Ingresar en modo publico")
    print("2. Ingresar con mi cuenta")
    print("3. Salir")
    opcion = int(input("Opcion: "))
    
    if (opcion == 1):
        ultimas10() 
    
    elif (opcion == 2):
        print('Que funcion desea realizar')
        print("1. Directores")
        print("2. Generos")
        print("3. Peliculas de un director")
        print("4. Peliculas con portada")
        print("5. Ver peliculas")
        print("6. Eliminar pelicula")
        print("7. Editar informacion de una pelicula")
        print("8. Agregar una pelicula")
        funcion = int(input("Funcion: "))
        
        if (funcion == 1):
            directores()
        
        elif (funcion == 2):
            generos()
        
        else:
            funcion = int(input('ERROR. Opcion invalida, vuelva a ingresar su opcion: '))
            print()
        
        
    
    elif (opcion == 3):
        exit()
        
    
    else:
        opcion = int(input('ERROR. Opcion invalida, vuelva a ingresar su opcion: '))
        print()



