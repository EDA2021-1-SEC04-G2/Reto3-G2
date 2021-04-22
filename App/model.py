"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert cf


# Construccion de modelos

def new_catalog():

    catalog = {'events': None,
                'instrumentalness_index': None
                }

    catalog['events'] = m.newMap(maptype='Probing',loadfactor=0.5)
    catalog['instrumentalness_index'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare_instrumentalness)
    return catalog

# Funciones para agregar informacion al catalogo

def add_event(catalog, event):
    tupla=event['created_at'],event['user_id'],event['track_id']
    m.put(catalog['events'],tupla,event)
    update_instrumentalness_index(catalog['instrumentalness_index'], event)
    return catalog

def update_instrumentalness_index(map, event):
   
    instrumentalness = event['instrumentalness']
    entry = om.get(map, instrumentalness)
    if entry is None:
        dataentry = new_data_entry()
        om.put(map, instrumentalness, dataentry)
    else:
        dataentry = me.getValue(entry)
    add_instrumentalness_index(dataentry, event)
    return map

def add_hashtag(event2,catalog):
    tupla=event2['created_at'],event2['user_id'],event2['track_id']
    entry=m.get(catalog['events'],tupla)
    contador=0
    if entry!=None:
       event1=me.getValue(entry)
       event1['hashtag']=event2['hashtag']
       contador+=1

    

# Funciones para creacion de datos

def add_instrumentalness_index(dataentry, event):
   
    lst = dataentry['lstevents']
    lt.addLast(lst, event)
    return dataentry

def new_data_entry():
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'lstevents': None}
    entry['lstevents'] = lt.newList('ARRAY_LIST', cmpfunction=compare_event_ids)
    return entry


# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compare_instrumentalness(instrumentalness1, instrumentalness2):
    """
    Compara dos fechas
    """
    if (instrumentalness1 == instrumentalness2):
        return 0
    elif (instrumentalness1 > instrumentalness2):
        return 1
    else:
        return -1

def compare_event_ids(id1, id2):
 
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

# Funciones de ordenamiento
