﻿"""
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
from DISClib.Algorithms.Sorting import mergesort as merge
import datetime
assert cf


# Construccion de modelos

def new_catalog():

    catalog = {}

    catalog['events'] = m.newMap(maptype='Probing',loadfactor=0.5)

    catalog['artists']=m.newMap(maptype='Probing',loadfactor=0.5)

    catalog['tracks']=m.newMap(maptype='Probing',loadfactor=0.5)

    catalog['values']=m.newMap(maptype='Probing',loadfactor=0.5)
   
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
    catalog['times']=om.newMap(omaptype='RBT',
                                      comparefunction=compare_characteristic)
    catalog['tempo_generos_editable']={'Reggae':(60,90),
                              'Down-tempo':(70,100),
                              'Chill-out':(90,120),
                              'Hip-hop':(85,115),
                              'Jazz and Funk':(120,125),
                              'Pop':(100,130),
                              'R&B':(60,80),
                              'Rock':(110,140),
                              'Metal':(100,160)}
   
    catalog['tempo_generos']={'Reggae':(60,90),
                              'Down-tempo':(70,100),
                              'Chill-out':(90,120),
                              'Hip-hop':(85,115),
                              'Jazz and Funk':(120,125),
                              'Pop':(100,130),
                              'R&B':(60,80),
                              'Rock':(110,140),
                              'Metal':(100,160)}
    return catalog

# Funciones para agregar informacion al catalogo

def add_event(catalog, event):
    tupla=event['created_at'],event['user_id'],event['track_id']
    if not m.contains(catalog['events'],tupla):
         m.put(catalog['events'],tupla,event)
         m.put(catalog['artists'],event['artist_id'],None)
         m.put(catalog['tracks'],event['track_id'],event)
         update_characteristic_index(catalog['instrumentalness_index'], event,'instrumentalness')
         update_characteristic_index(catalog['liveness_index'], event,'liveness')
         update_characteristic_index(catalog['speechiness_index'], event,'speechiness')
         update_characteristic_index(catalog['danceability_index'], event,'danceability')
         update_characteristic_index(catalog['valence_index'], event,'valence')
         update_characteristic_index(catalog['acousticness_index'], event,'acousticness')
         update_characteristic_index(catalog['energy_index'], event,'energy')
         update_characteristic_index(catalog['tempo_index'], event,'tempo')
         update_characteristic_index(catalog['times'], event,'created_at')
    return catalog

def add_values(value,catalog):
    m.put(catalog['values'],value['hashtag'],value)

def update_characteristic_index(map, event,characteristic):
   
    if characteristic=='created_at':
         hora = event['created_at']
         hora = datetime.datetime.strptime(hora, '%Y-%m-%d %H:%M:%S')
         hora=hora.time()
         characteristic_value=hora
    else:
        characteristic_value = float(event[characteristic])
    entry = om.get(map, characteristic_value)
    if entry is None:
        entry = new_entry()
        om.put(map, characteristic_value,entry)
    else:
        entry = me.getValue(entry)
    add_characteristic_index(entry, event)
    return map

def add_hashtag(event2,catalog):
    tupla = event2['created_at'],event2['user_id'],event2['track_id']
    entry=m.get(catalog['events'],tupla)
    hashtag=event2['hashtag'].lower()
    if entry!=None:
       event1=me.getValue(entry)
       if 'hashtag' not in event1:
           event1['hashtag']=lt.newList('ARRAY_LIST')
       lt.addLast(event1['hashtag'],hashtag)
    else:
        event2['hashtag']=lt.newList('ARRAY_LIST')
        lt.addLast(event2['hashtag'],hashtag)
        m.put(catalog['events'],tupla,event2)
    

# Funciones para creacion de datos

def add_characteristic_index(entry, event):
   
    lst = entry['lstevents']
    lt.addLast(lst, event)
    m.put(entry['artists'],event['artist_id'],None)
    m.put(entry['tracks'],event['track_id'],event)
    return entry

def new_entry():
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'lstevents': None,'artsits':None}
    entry['lstevents'] = lt.newList('ARRAY_LIST')
    entry['artists']=m.newMap(maptype='Probing',loadfactor=0.5)
    entry['tracks']=m.newMap(maptype='Probing',loadfactor=0.5)
    return entry


# Funciones de consulta
def get_events_characteristic(catalog,characteristic_index,lo,hi):
    characteristic_tree=catalog[characteristic_index]
    lst=om.values(characteristic_tree,lo,hi)
    totevents=0
    artists=m.newMap(maptype='Probing',loadfactor=0.5)
    for entry in lt.iterator(lst):
        totevents+=lt.size(entry['lstevents'])
        for artist in lt.iterator(m.keySet(entry['artists'])):
            m.put(artists,artist,None)
    return totevents,m.size(artists),m.keySet(artists)

def get_tracks_party(catalog,lo1,hi1,lo2,hi2):
    energy_tree=catalog['energy_index']
    lst=om.values(energy_tree,lo1,hi1)
    energy_dance_list=lt.newList('ARRAY_LIST')
    for entry in lt.iterator(lst):
        for track in lt.iterator(m.valueSet(entry['tracks'])):
            if lo2<=float(track['danceability'])<=hi2:
                lt.addLast(energy_dance_list,track)
    return energy_dance_list

def get_tracks_study(catalog,lo1,hi1,lo2,hi2):
    intrumentalness_tree=catalog['instrumentalness_index']
    lst=om.values(intrumentalness_tree,lo1,hi1)
    instru_tempo_list=lt.newList('ARRAY_LIST')
    for entry in lt.iterator(lst):
        for track in lt.iterator(m.valueSet(entry['tracks'])):
            if lo2<=float(track['tempo'])<=hi2:
                lt.addLast(instru_tempo_list,track)
    return instru_tempo_list

def add_genre(catalog,generos,name,lo,hi):
    catalog['tempo_generos_editable'][name]=(lo,hi)
    generos.append(name)
    
def get_events_by_genero(catalog,generos):
    total=0
    lista=lt.newList('ARRAY_LIST')
    for genero in generos:
        lo=catalog['tempo_generos_editable'][genero][0]
        hi=catalog['tempo_generos_editable'][genero][1]
        ans_genero=get_events_characteristic(catalog,'tempo_index',lo,hi),genero,lo,hi
        lt.addLast(lista,ans_genero)
        total+=ans_genero[0][0]
    return total,lista

def get_vader(catalog, arreglo,total):
    entry_most_rep = lt.getElement(arreglo,1)
    tracks = entry_most_rep[2]
    tracks = m.valueSet(tracks)
    lista=lt.newList('ARRAY_LIST')
    for track in lt.iterator(tracks):
        hashtags = track['hashtag']
        suma = 0 
        mean = 0
        for hashtag in lt.iterator(hashtags):
            entry = m.get(catalog["values"], hashtag)
            if entry is not None:
                sentiments=me.getValue(entry)
                vader = sentiments["vader_avg"]
                if vader != "":
                    vader = float(vader)
                    suma += vader
                
        if lt.size(hashtags) != 0:
            mean = suma/lt.size(hashtags)
        lt.addLast(lista,(track["track_id"],lt.size(hashtags), mean))
    return lista,arreglo,total

def req5(catalog,lo,hi):
    lst=om.values(catalog['times'],lo,hi)
    arreglo=lt.newList('ARRAY_LIST')
    total=0
    for genero in catalog['tempo_generos']:
        mapa=m.newMap(10,maptype='Probing',loadfactor=0.5)
        entry=[genero,0,mapa]
        lt.addLast(arreglo,entry)

    for nodo in lt.iterator(lst):
        for event in lt.iterator(nodo['lstevents']):
            i=1
            total+=1
            for genero in catalog['tempo_generos']:
                lo=catalog['tempo_generos'][genero][0]
                hi=catalog['tempo_generos'][genero][1]
                if lo<=float(event['tempo'])<=hi:
                    entry=lt.getElement(arreglo,i)
                    entry[1]+=1
                    m.put(entry[2],event['track_id'],event)
                i+=1
    arreglo = merge.sort(arreglo,comparar_info_req5)
    return get_vader(catalog,arreglo,total)

def events_size(catalog):
    return m.size(catalog['events'])

def artists_size(catalog):
    return m.size(catalog['artists'])

def tracks_size(catalog):
    return m.size(catalog['tracks'])

def events_list(catalog):
    return m.valueSet(catalog['events'])



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

def comparar_info_req5(entry1,entry2):
    return entry1[1]>entry2[1]

def comparar_hashtags(tupla1,tupla2):
    return tupla1[1]>tupla2[1]

# Funciones de ordenamiento
