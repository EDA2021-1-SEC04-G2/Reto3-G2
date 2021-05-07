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
 """

import config as cf
import time
import tracemalloc
import model
import csv
from DISClib.ADT import list as lt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init_catalog():
    catalog = model.new_catalog()
    return catalog


# Funciones para la carga de datos
def load_data(catalog):
    load_events1(catalog)
    load_events2(catalog)


def load_events1(catalog):
    eventsfile = cf.data_dir + 'subsamples-small/context_content_features-small.csv'
    input_file = csv.DictReader(open(eventsfile, encoding='utf-8'))
    for event in input_file:
        model.add_event(catalog, event)
    
        

def load_events2(catalog):
    eventsfile = cf.data_dir + 'subsamples-small/user_track_hashtag_timestamp-small.csv'
    input_file = csv.DictReader(open(eventsfile, encoding='utf-8'))
    for event2 in input_file:
        model.add_hashtag(event2,catalog)
 


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def get_events_characteristic(catalog,characteristic_index,lo,hi):
    ans = None
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    ans = model.get_events_characteristic(catalog,characteristic_index,lo,hi)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return ans,delta_time, delta_memory

def get_tracks_party(catalog,lo1,hi1,lo2,hi2):
    ans = None
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    ans = model.get_tracks_party(catalog,lo1,hi1,lo2,hi2)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return ans,delta_time, delta_memory

def get_tracks_study(catalog,lo1,hi1,lo2,hi2):
    ans = None
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    ans = model.get_tracks_study(catalog,lo1,hi1,lo2,hi2)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return ans,delta_time, delta_memory

def add_genre(catalog,generos,name,lo,hi):
    return model.add_genre(catalog,generos,name,lo,hi)

def get_events_by_genero(catalog,generos):
    ans = None
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    ans = model.get_events_by_genero(catalog,generos)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return ans,delta_time, delta_memory

def events_size(catalog):
    return model.events_size(catalog)

def artists_size(catalog):
    return model.artists_size(catalog)

def tracks_size(catalog):
    return model.tracks_size(catalog)


# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
