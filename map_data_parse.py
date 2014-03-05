#!/usr/bin/env python
import subprocess
import json
import os
from pprint import pprint
import numpy as np
import shutil

try:
    os.remove('map_data/countries.json')
except OSError:
    pass
proc_args = 'ogr2ogr -f GeoJSON -where "ADM0_A3=\'MEX\'" map_data/countries.json map_data/ne_10m_admin_0_map_subunits/ne_10m_admin_0_map_subunits.shp'
proc = subprocess.Popen(proc_args, shell=True)
proc.wait()

try:
    os.remove('map_data/states.json')
except OSError:
    pass
proc_args = 'ogr2ogr -f GeoJSON -where "iso_3166_2 IN (\'US-CA\', \'US-OR\', \'US-NV\', \'US-ID\', \'US-UT\', \'US-AZ\')" map_data/states.json map_data/ne_10m_admin_1_states_provinces_lakes/ne_10m_admin_1_states_provinces_lakes.shp'
proc = subprocess.Popen(proc_args, shell=True)
proc.wait()


states_file=open('map_data/states.json')
states_data = json.load(states_file)
arrays = []
for state in states_data['features']:
    if len(state['geometry']['coordinates']) == 1:
        arr =  np.array(state['geometry']['coordinates'][0])
        arrays.append(arr)
        #print arr.shape, np.amin(arr, axis=0), np.amax(arr, axis=0)
    else:
        for sub in state['geometry']['coordinates']:
            arr =  np.array(sub[0])
            arrays.append(arr)
            #print arr.shape, np.amin(arr, axis=0), np.amax(arr, axis=0)

all_coords = np.concatenate(arrays, axis=0)

min_coords = np.amin(all_coords, axis=0)
max_coords = np.amax(all_coords, axis=0)

states_file.close()

try:
    os.remove('map_data/urban-areas.json')
except OSError:
    pass
proc_args = 'ogr2ogr -f GeoJSON -where "SCALERANK < 8" -spat {xmin} {ymin} {xmax} {ymax} map_data/urban-areas.json map_data/ne_10m_urban_areas/ne_10m_urban_areas.shp'.format(
    xmin=min_coords[0],
    ymin=min_coords[1],
    xmax=max_coords[0],
    ymax=max_coords[1]
)
proc = subprocess.Popen(proc_args, shell=True)
proc.wait()

try:
    os.remove('map_data/places.json')
except OSError:
    pass
proc_args = 'ogr2ogr -f GeoJSON -where "SCALERANK < 5 AND ADM1NAME=\'California\'" map_data/places.json map_data/ne_10m_populated_places/ne_10m_populated_places.shp'.format(
    xmin=min_coords[0],
    ymin=min_coords[1],
    xmax=max_coords[0],
    ymax=max_coords[1]
)
proc = subprocess.Popen(proc_args, shell=True)
proc.wait()


try:
    os.remove('map.json')
except OSError:
    pass
proc_args = 'topojson -o static/map.json --id-property SU_A3,name,NAME -p name=NAME -p name -- countries=map_data/countries.json states=map_data/states.json places=map_data/places.json urban_areas=map_data/urban-areas.json'
proc = subprocess.Popen(proc_args, shell=True)
proc.wait()


