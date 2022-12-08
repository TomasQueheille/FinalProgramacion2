from flask import Flask, jsonify
app = Flask(__name__)
import json

pelis = json.loads("peliculas")

@app.route("/",methods=['GET'])
def modopublico():
    print("Modo Publico")
    print(pelis)
    #listapeliculas = []
    #return jsonify(listapeliculas)

#def modologueado():

while (True):
    print('MENU DE OPCIONES')
    print("1. Ingresar en modo publico")
    print("2. Ingresar con mi cuenta")
    print("3. Salir")
    opcion = int(input("Opcion: "))
    
    if (opcion == 1):
        modopublico()
    
    #elif (opcion == 2):
        #modologueado()
    
    elif (opcion == 3):
        exit()
    
    else:
        opcion = int(input('ERROR. Opcion invalida, vuelva a ingresar su opcion: '))
        print()