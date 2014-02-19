#!/usr/bin/env python

# This is used for development only. When pyvc is installed on pythonpath this
# is unnessecary.
import site
site.addsitedir('')

from pyvc import *


from flask import Flask, request, url_for, redirect


import json

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def test():
    return app.send_static_file('index.html')
    #return redirect(url_for('static', filename='index.html'))


@app.route('/webvc', methods=['GET'])
def webvc():
    sim_file = 'data/ALLCAL2_1-7-11_no-creep_dyn-05_st-20.h5'
    if request.method == 'GET':
        if request.args.get('fault_geometry') == 'true':
            return fault_geometry(sim_file)

def fault_geometry(sim_file):
    with VCSimData() as sim_data:
        sim_data.open_file(sim_file)
        
        geometry = VCGeometry(sim_data)

        return json.dumps(geometry.get_fault_traces())

if __name__ == '__main__':
    app.run(debug=True)