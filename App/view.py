"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def print_menu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Caracterizar reproducciones por caracteristica")
    print("3- Encontrar musica para festejar")
    print("4- Encontrar musica para estudiar")
    print("5- Estudiar los generos musicales")
    print("6- Encontrar el genero musical mas escuchado en el tiempo")
    print("0- Salir")

def init_catalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.init_catalog()


def load_data(catalog):
    """
    Carga los libros en la estructura de datos
    """
    controller.load_data(catalog)

def print_loads(catalog):
    print('Se han cargado',controller.events_size(catalog),'eventos de reproducción')
    print('Se han registrado',controller.artists_size(catalog),'artistas diferentes')
    print('Se han registrado',controller.tracks_size(catalog),'canciones diferentes')
    eventos=controller.events_list(catalog)
    i=1
    while i<=10 and i<=lt.size(eventos):
        #TODO poner las vainas estas
        evento=lt.getElement(eventos,i)
        print('El evento número',i,)
        i+=1
        
def print_req1(catalog,ans):
    print('---RESULTADOS REQ. 1---')
    print('Total de reproducciones: ',ans[0],'Total de artistas diferentes: ',ans[1])

def print_req2(catalog,lo1,hi1,lo2,hi2,ans):
    print('---RESULTADOS REQ. 2---')
    print('La energía está entre',lo1,'y',hi1)
    print('La danzabilidad está entre',lo1,'y',hi1)
    print('Se identificaron un total de',lt.size(ans),'canciones diferentes')
    print('--Id único de canción--')
    i=1
    while i<=5 and i<=lt.size(ans):
        #TODO random
        track=lt.getElement(ans,i)
        print('Canción '+str(i)+':',track['track_id'],'con energía',track['energy'],'y danzabilidad',track['danceability'])
        i+=1

def print_req3(catalog,lo1,hi1,lo2,hi2,ans):
    print('---RESULTADOS REQ. 3---')
    print('La instrumentalidad está entre',lo1,'y',hi1)
    print('El tempo está entre',lo1,'y',hi1)
    print('Se identificaron un total de',lt.size(ans),'canciones diferentes')
    print('--Id único de canción--')
    i=1
    while i<=5  and i<=lt.size(ans):
        #TODO random
        track=lt.getElement(ans,i)
        print('Canción '+str(i)+':',track['track_id'],'con instrumentalidad',track['instrumentalness'],'y tempo',track['tempo'])
        i+=1

def print_req4(catalog, ans):
    print('---RESULTADOS REQ. 4---')
    print('La cantidad de reproducciones totales es:',ans[0])
    for entry in lt.iterator(ans[1]):
        print('---',entry[1].upper(),'---')
        print('Para',entry[1],'el tempo está entre',entry[2],'y',entry[3],'BPM')
        print('Se han registrado',entry[0][0],'reproducciones y',entry[0][1],'diferentes artistas')
        print('--- Algunos artistas de',entry[1],'---')
        i=1
        while i<=5 and i<=lt.size(entry[0][2]):
            artist=lt.getElement(entry[0][2],i)
            print('Artista '+str(i)+':',artist)
            i+=1

catalog = None

"""
Menu principal
"""
while True:
    print_menu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = init_catalog()
        load_data(catalog)
        print_loads(catalog)
    elif int(inputs[0]) == 2:
        characteristic_index=input('Ingrese la característica que desea utilizar: ')+'_index'
        lo=float(input('Mínimo valor de la caractersitica: '))
        hi=float(input('Máximo valor de la caracteristica: '))
        ans=controller.get_events_characteristic(catalog,characteristic_index,lo,hi)
        print_req1(catalog,ans[0])
        print(round(ans[1],3),'[ms]',round(ans[2],3),'[kb]')
    elif int(inputs[0]) == 3:
        lo1=float(input('El mínimo valor de "energy": '))
        hi1=float(input('El máximo valor de "energy": '))
        lo2=float(input('El mínimo valor de "danceability": '))
        hi2=float(input('El máximo valor de "danceability": '))
        ans=controller.get_tracks_party(catalog,lo1,hi1,lo2,hi2)
        print_req2(catalog,lo1,hi1,lo2,hi2,ans[0])
        print(round(ans[1],3),'[ms]',round(ans[2],3),'[kb]')
    elif int(inputs[0]) == 4:
        lo1=float(input('El mínimo valor de "instrumentalness": '))
        hi1=float(input('El máximo valor de "instrumentalness": '))
        lo2=float(input('El mínimo valor de "tempo": '))
        hi2=float(input('El máximo valor de "tempo": '))
        ans=controller.get_tracks_study(catalog,lo1,hi1,lo2,hi2)
        print_req3(catalog,lo1,hi1,lo2,hi2,ans[0])
        print(round(ans[1],3),'[ms]',round(ans[2],3),'[kb]')
    elif int(inputs[0]) == 5:
        print('Los géneros registrados son')
        print('Reggae')
        print('Down-tempo')
        print('Chill-out')
        print('Hip-hop')
        print('Jazz and Funk')
        print('Pop')
        print('R&B')
        print('Rock')
        print('Metal')
        generos=input('Ingrese los géneros que desea buscar: ')
        generos=generos.split(',')
        nuevo=True
        while nuevo:
            nuevo=input('¿Desea registrar un género nuevo?: ').lower()
            nuevo= nuevo=='si'
            if nuevo:
                name=input('Ingrese el nombre del género: ')
                lo=float(input('Valor mínimo del Tempo del género musical: '))
                hi=float(input('Valor máximo del Tempo del género musical: '))
                controller.add_genre(catalog,generos,name,lo,hi)
        ans=controller.get_events_by_genero(catalog,generos)
        print_req4(catalog,ans[0])
        print(round(ans[1],3),'[ms]',round(ans[2],3),'[kb]')
    elif int(inputs[0]) == 6:
        lo=input('Ingrese hora min: ')
        hi=input('Ingrese hora max: ')
        print(controller.req5(catalog,lo,hi))
    else:
        sys.exit(0)
sys.exit(0)