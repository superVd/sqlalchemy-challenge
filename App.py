import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import flask
from flask import Flask, jsonify


#----------------------------------------
#         Database Setup
#----------------------------------------
engine = create_engine("sqlite:///C:/Users/Victor M Diaz/Documents/SQLAlchemy HW/hawaii.sqlite")

#convert databse into a new model
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#table referance
Measurement = Base.classes.measurement
Station = Base.classes.station

#create the session that connects from python to database
session = Session(engine)


#-----------------------------------------------
#                Setup Flask
#-----------------------------------------------
app = Flask(__name__)

#----------------------------------------------
#Setup flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hi Welcome To Flask Assignment:<br/>"
           f"<br/>"
        f"/api/v1.0/precipitation<br/>"
           f"- The List of station with  prior year rain totals <br/>"
           f"<br/>"
        f"/api/v1.0/stations<br/>"
           f"- List of all Station numbers and names<br/>"
           f"<br/>"
        f"/api/v1.0/tobs<br/>"
           f"- The List of prior with year temperatures from all stations<br/>"
           f"<br/>"
        f"/api/v1.0/start<br/>"
           f"- Calculates the MIN, AVG, and MAX temperature of the dates greater than and equal to the start date<br/>"
           f"<br/>"
        f"/api/v1.0/start/end<br/>"
           f"- Calculate the MIN, AVG , and MAX temperature for dates from start and end date<br/>"

    )
            
#----------------------------------------------------------- 
# add precipitation to app 
@app.route("/api/v1.0/precipitation")
def precipitation():
    LastMonth_prec = session.query(Measurement.prcp , Measurement.date).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()
    predict = {date : x for date , x in LastMonth_prec}
    return jsonify(predict)

#-------------------------------------------------------------
# add station to app
@app.route("/api/v1.0/stations")
def station():
    result = session.query(Station.station).all()
    all_stations = list(np.ravel(result))
    return jsonify (all_stations)


#-------------------------------------------------------------
#add tobs 
@app.route("/api/v1.0/tobs")
def tobs():
    tobss = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281' ).\
            filter(Measurement.date >= '2017,8,23').all()
    tobs_list = list(np.ravel(tobss))
    return jsonify (tobs_list)

#-------------------------------------------------------------
#add start and end
@app.route ("/api/v1.0/<start>/<end>")
def temps(start,end):
    findings = session.query(Measurement).filter(Measurement.date>= start).filter(Measurement.date<=end)
    found =[] 
    for row in findings:
        found.append(row.tobs) 
    return (jsonify ({"tempmin": min(found),"tempmax": max(found),"tempavg":np.mean}))
           
#-------------------------------------------------------------            
if __name__ == "__main__":
   app.run(debug=True)



   