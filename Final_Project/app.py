#________*_________*_________*_________*_________*_________*_________*_________*
# SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Flask things
from flask import Flask, render_template, jsonify, request, redirect

#pandas for data manipulation and export
import pandas as pd
import numpy as np

#import queries
from race_query import race_query, race_columns, pie_query

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#________*_________*_________*_________*_________*_________*_________*_________*
db_uri = "sqlite:///db.sqlite"
engine = create_engine(db_uri, echo = False)
#________*_________*_________*_________*_________*_________*_________*_________*
#### HOME PAGE #####
@app.route("/")
def home():
    return render_template("index.html")
    #return render_template("indextest.html")
#________*_________*_________*_________*_________*_________*_________*_________*
#### PRESENTATION #####
@app.route("/presentation")
def prez():
    return render_template("presentation.html")
#________*_________*_________*_________*_________*_________*_________*_________*
#### PRESENTATION #####
@app.route("/conclusions")
def conclusions():
    return render_template("conclusions.html")

#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_________*_________*_________*_________*_________*_________*


#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_________*_________*_________*_________*_________*_________*

#### BUBBLE #####
@app.route("/fcc/<string:region>")
def fcc(region):
    query = f"SELECT * FROM FCC WHERE Region = '{region}'" 
    results = engine.execute(query)
    fcc = []
    dbaname = []
    service_count = []
    maxaddown = []
    maxadupload = []
    region = []
    for result in results:
        dbaname.append(result[1])
        maxaddown.append(result[2])
        maxadupload.append(result[3])
        region.append(result[5])
        service_count.append(result[6])

    fcc_dictionary = {
        "dbaname": dbaname,
        'maxaddown': maxaddown,
        'maxadupload': maxadupload,
        'region': region,
        "service_count": service_count,
                        }        
    return jsonify(fcc_dictionary)
#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_________*_________*_________*_________*_________*_________*
#### PIE #####
@app.route("/pie/<string:region>/")
def pie(region='northwest'):
    results = engine.execute(pie_query.format(region))
    white = []
    native = []
    black = []
    asian = []
    hawaiian = []
    other = []
    two_plus = []
    labels = ['white','native','black','asian','hawaiian','other','two_plus']
    for row in results:
        white.append(row[0])
        native.append(row[1])
        black.append(row[2])
        asian.append(row[3])
        hawaiian.append(row[4])
        other.append(row[5])
        two_plus.append(row[6]) 

    pie_data = [{
        "labels": labels,
        "values": [sum(white), sum(native), sum(black), sum(asian), sum(hawaiian), sum(other),sum(two_plus)],
        "type": "pie"
    }]
    return jsonify(pie_data)
#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_________*_________*_________*_________*_________*_________*
#### BAR #####
@app.route("/bar/<string:region>/")
def barchart(region='northwest'):
    results = engine.execute(race_query.format(region))

    white = []
    native = []
    black = []
    asian = []
    hawaiian = []
    other = []
    two_plus = []
    white_int = []
    native_int = []
    black_int= []
    asian_int = []
    hawaiian_int = []
    other_int = []
    two_plus_int = []
    labels = ['white','native','black','asian','hawaiian','other','two_plus']
    for row in results:
        white.append(int(row[0]))
        native.append(int(row[1]))
        black.append(int(row[2]))
        asian.append(int(row[3]))
        hawaiian.append(int(row[4]))
        other.append(int(row[5]))
        two_plus.append(int(row[6]))
        white_int.append(int(row[8]))
        native_int.append(int(row[9]))
        black_int.append(int(row[10]))
        asian_int.append(int(row[11]))
        hawaiian_int.append(int(row[12]))
        other_int.append(int(row[13]))
        two_plus_int.append(int(row[14]))
    bar_data = {
        "x": labels,
        "y": [sum(white_int)*100/sum(white), sum(native_int)*100/sum(native), sum(black_int)*100/sum(black), sum(asian_int)*100/sum(asian), sum(hawaiian_int)*100/sum(hawaiian), sum(other_int)*100/sum(other),sum(two_plus_int)*100/sum(two_plus)],
        "type": "bar"
    }
    return jsonify(bar_data)

#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_________*_________*_________*_________*_________*_________*
#### MAP #####
@app.route("/map/<string:region>/")
def mapit(region='northwest'):
    mapquery = f"select Latitude, Longitude, Region, county_name, fips_id, PE_Computer_Broadband_Household, E_Computer_Broadband_Household FROM census where Region = '{region}'"
    results = engine.execute(mapquery)
    census=[]
    for row in results:
        mydict = {
            "latitude": row[0], 
            "longitude": row[1],
            "region": row[2],
            "county": row[3],
            "tract": row[4],
            "pct_has_computer_and_broadband": row[5],
            "has_computer_and_broadband": row[6]
            } #{"latitude": row[0]}
        census.append(mydict)
    return jsonify(census)




#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_________*_________*_________*_________*_________*_________*
if __name__ == "__main__":
    app.run(debug=True)
#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_________*_________*_________*_________*_________*_________*



    
    # white_int_sum = sum(white_int)
    # native_int_sum = sum(native_int)
    # black_int_sum = sum(black_int)
    # asian_int_sum = sum(asian_int)
    # hawaiian_int_sum = sum(hawaiian_int)
    # other_int_sum = sum(other_int)
    # two_plus_int_sum = sum(two_plus_int_sum)

    # from __future__ import division
    # white_per = []
    # native_per = []
    # black_per= []
    # asian_per = []
    # hawaiian_per = []
    # other_per = []
    # two_plus_per = []

    # white_per = [x/y for x, y in zip(white_int, white)]
    # native_per = [x/y for x, y in zip(native_int, native)]
    # black_per = [x/y for x, y in zip(black_int, black)]
    # asian_per = [x/y for x, y in zip(asian_int, asian)]
    # hawaiian_per = [x/y for x, y in zip(hawaiian_int, hawaiian)]
    # other_per = [x/y for x, y in zip(other_int, other)]
    # two_plus_per = [x/y for x, y in zip(two_plus_int, two_plus)]
        
        #,
            #"_ci" : row[7],
            # "wci" : row[8],
            # "nci" : row[9],
            # "bci" : row[10],
            # "aci" : row[11],
            # "hci" : row[12],
            # "oci" : row[13],
            # "tci" : row[14],
            # "_cni": row[15],
            # "wcni" : row[16],
            # "ncni" : row[17],
            # "bcni" : row[18],
            # "acni" : row[19],
            # "hcni" : row[20],
            # "ocni" : row[21],
            # "tcni" : row[22],
            # "hl_any" : row[23],
            # "w_not_hl" : row[24],
            # "hl_any_ci" : row[25],
            # "w_not_hl_ci" : row[26],
            # "ncw" : row[27],
            # "ncn" : row[28],
            # "ncb" : row[29],
            # "nca" : row[30],
            # "nc_hl_any" : row[31],
            # "nc_w_not_hl" : row[32],

            #### TREEMAP #####
'''@app.route("/treemap/<string:region>")
def treemap():
        results = engine.execute(pie_query.format(region))
    white = []
    native = []
    black = []
    asian = []
    hawaiian = []
    other = []
    two_plus = []
var total= ["Race", None]
    var total= ["White","Race"]
    var total= ["With Computer, White", "White"]
    var total= ["No Computer, White", "White"]
    var total= ["With Internet", "With Computer, White"]
    var total= ["American Indian or Alaska Native","Race"],
    var total= ["With Computer, Indigenous", "American Indian or Alaska Native"]
    var total= ["No Computer, Indigenous", "American Indian or Alaska Native"]
    var total= ["With Internet", "With Computer, Indigenous"]
    var total= ["Asian","Race"],
    var total= ["With Computer, Asian", "Asian"]
    var total= ["No Computer, Asian", "Asian"]
    var total= ["With Internet", "With Computer, Asian"]
    var total= ["Native Hawaiian/Other Pacific Islander", "Race"]
    var total= ["Other", "Race"]
    var total= ["Two or more Races", "Race"]

    ["race", none, data_frame.iloc[0,0]] 
    for x in range.length()
        white.append(row[0])
        native.append(row[1])
        black.append(row[2])
        asian.append(row[3])
        hawaiian.append(row[4])
        other.append(row[5])
        two_plus.append(row[6])
            #"_ci" : row[7],
            # "wci" : row[8],
            # "nci" : row[9],
            # "bci" : row[10],
            # "aci" : row[11],
            # "hci" : row[12],
            # "oci" : row[13],
            # "tci" : row[14],
            # "_cni": row[15],
            # "wcni" : row[16],
            # "ncni" : row[17],
            # "bcni" : row[18],
            # "acni" : row[19],
            # "hcni" : row[20],
            # "ocni" : row[21],
            # "tcni" : row[22],
            # "hl_any" : row[23],
            # "w_not_hl" : row[24],
            # "hl_any_ci" : row[25],
            # "w_not_hl_ci" : row[26],
            # "ncw" : row[27],
            # "ncn" : row[28],
            # "ncb" : row[29],
            # "nca" : row[30],
            # "nc_hl_any" : row[31],
            # "nc_w_not_hl" : row[32],
            '''