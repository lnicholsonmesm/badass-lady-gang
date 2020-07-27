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
#### BAR #####
@app.route("/bar/<region>")
def apitest(region):
    census = []
    mapquery = f"select Latitude, Longitude, Region, county_name, fips_id, PE_Computer_Broadband_Household, E_Computer_Broadband_Household FROM census where Region = '{region}'"
    results = engine.execute(mapquery)
    
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
#### BUBBLE #####
@app.route("/fcc/<string:region>")
def fcc(region):
    query = "SELECT * FROM FCC" 
    #f"SELECT dbaname, maxaddown, Region FROM fcc WHERE Region = '{region}'"# GROUP BY dbaname, Region" #, COUNT(consumer) as service_count   and consumer = 1 
    #print(query)
    results = engine.execute(query) #.fetchall()
    #fcc_df_qry = pd.DataFrame(results)
    #print(fcc_df_qry[11])
    
    fcc = []
    dbaname = []
    service_count = []
    maxaddown = []
    maxadupload = []
    region = []
    for result in results:
        #print(result[11])
       # if result[11]==region:
            #print(result)
        dbaname.append(result[1])
        maxaddown.append(result[2])
        maxadupload.append(result[3])
        region.append(result[5])
       # service_count.append(result[7] if result[7] == 1 else 0)
        service_count.append(result[6])

    fcc_dictionary = {
        "dbaname": dbaname,
        'maxaddown': maxaddown,
        'maxadupload': maxadupload,
        'region': region,
        "service_count": service_count,
                        }        
    #"dbaname","hocofinal","stateabbr","blockcode", "tract", "techcode",
    #"consumer","maxaddown","maxadup"]]
    return jsonify(fcc_dictionary)

#________*_________*_________*_________*_________*_________*_________*_________*
#### PIE #####
@app.route("/treemap/<string:region>/")
def treemap(region='northwest'):
    
    #print(race_query.format(region))
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
        two_plus.append(row[6]) #,
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

    pie_data = [{
        "labels": labels,
        "values": [sum(white), sum(native), sum(black), sum(asian), sum(hawaiian), sum(other),sum(two_plus)],
        "type": "pie"
    }]
    return jsonify(pie_data)
#________*_________*_________*_________*_________*_________*_________*_________*

#### MAP #####
@app.route("/map/<string:region>/")
def treemap(region='northwest'):

if __name__ == "__main__":
    app.run(debug=True)
