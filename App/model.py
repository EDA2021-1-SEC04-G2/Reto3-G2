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

    catalog = {}

    catalog['events'] = lt.newList('ARRAY_LIST')

    catalog['artists']=m.newMap(maptype='Probing',loadfactor=0.5)
   
    catalog['instrumentalness_index'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare_characteristic)
    catalog['liveness_index'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare_characteristic)
    catalog['speechiness_index'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare_characteristic)
    catalog['danceability_index'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare_characteristic)
    catalog['valence_index'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare_characteristic)
    catalog['acousticness_index'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare_characteristic)
    catalog['energy_index'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare_characteristic)
    catalog['tempo_index'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare_characteristic)
    return catalog

# Funciones para agregar informacion al catalogo

def add_event(catalog, event):
    lt.addLast(catalog['events'],event)
    m.put(catalog['artists'],event['artist_id'],None)
    update_characteristic_index(catalog['instrumentalness_index'], event,'instrumentalness')
    update_characteristic_index(catalog['liveness_index'], event,'liveness')
    update_characteristic_index(catalog['speechiness_index'], event,'speechiness')
    update_characteristic_index(catalog['danceability_index'], event,'danceability')
    update_characteristic_index(catalog['valence_index'], event,'valence')
    update_characteristic_index(catalog['acousticness_index'], event,'acousticness')
    update_characteristic_index(catalog['energy_index'], event,'energy')
    update_characteristic_index(catalog['tempo_index'], event,'tempo')
    return catalog

def update_characteristic_index(map, event,characteristic):
   
    characteristic_value = event[characteristic]
    entry = om.get(map, characteristic_value)
    if entry is None:
        dataentry = new_data_entry()
        om.put(map, characteristic_value, dataentry)
    else:
        dataentry = me.getValue(entry)
    add_characteristic_index(dataentry, event)
    return map

def add_hashtag(event2,catalog):
    return None
    tupla=event2['created_at'],event2['user_id'],event2['track_id']
    entry=m.get(catalog['events'],tupla)
    if entry!=None:
       event1=me.getValue(entry)
       event1['hashtag']=event2['hashtag']
   
       

    

# Funciones para creacion de datos

def add_characteristic_index(dataentry, event):
   
    lst = dataentry['lstevents']
    lt.addLast(lst, event)
    m.put(dataentry['artists'],event['artist_id'],None)
    return dataentry

def new_data_entry():
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'lstevents': None,'artsits':None}
    entry['lstevents'] = lt.newList('ARRAY_LIST', cmpfunction=compare_event_ids)
    entry['artists']=m.newMap(maptype='Probing',loadfactor=0.5)
    return entry


# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compare_characteristic(characteristic1, characteristic2):
    """
    Compara dos fechas
    """
    if (characteristic1 == characteristic2):
        return 0
    elif (characteristic1 > characteristic2):
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
