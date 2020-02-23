# Dependencies Setup
#################################################
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
#################################################
app = Flask(__name__)


# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome to the Climate APP<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>" )


# Queries and JSON Lists Return 
#1.Date:Pecipitation (2016-08-23----2017-08-23)
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    results_prcp=session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date <'2017-08-24').\
    filter(Measurement.date > '2016-08-22').all() 
    session.close()
    # Convert list of tuples into dictionary and return JSON file   
    #res_prcp=dict((idx[0],idx[1]) for idx in results_prcp)
    all_precipitations=[]
    for result in results_prcp:
        prcp_dict={result.date:result.prcp}
        all_precipitations.append(prcp_dict)
    return jsonify(all_precipitations)


#2.Stations   
@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    results_station=session.query(\
    Station.station, Station.name,\
    Station.latitude, Station.longitude,Station.elevation).all() 
    session.close()
    # Convert list of tuples into list and return JSON file 
    all_stations=[]
    for station,name,latitude,longitude,elevation in results_station:
        station_dict={}
        station_dict['station']=station
        station_dict['name']=name
        station_dict['latitude']=latitude
        station_dict['longitude']=longitude
        station_dict['elevation']=elevation
        all_stations.append(station_dict)
    return jsonify(all_stations)



#3.Temperatures
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    results_tobs=session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date <'2017-08-24').\
    filter(Measurement.date > '2016-08-22').all() 
    session.close()
    # Convert list of tuples into dictionary and return JSON file
    res_tobs=[]
    for date, tobs in results_tobs:
        res_tobs_dict={}
        res_tobs_dict["date"]=date
        res_tobs_dict["tobs"]=tobs
        res_tobs.append(res_tobs_dict)
    return jsonify(res_tobs)



#4.Start_date dynamic url
@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    # Create our session (link) from Python to the DB
    session=Session(engine)
    # Query
    results = session.query(func.max(Measurement.tobs), \
                            func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start_date).all()
    session.close()
    # Convert list of tuples into dictionary and return JSON file
    start_temp=[]
    for min_tob,avg_tob,max_tob in results:
        start_temp_dict={}
        start_temp_dict["Minium_Temperature"]=min_tob
        start_temp_dict["Average_Temperature"]=avg_tob
        start_temp_dict["Max_Temperature"]=max_tob
        start_temp.append(start_temp_dict)   
    return jsonify(start_temp)




#5.Start_date, end_date dynamic url 
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB
    session=Session(engine)
    # Query
    dresults = session.query(func.max(Measurement.tobs), \
                            func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date > start_date).\
                            filter(Measurement.date < end_date).all()   
    session.close()
    # Convert list of tuples into dictionary and return JSON file
    start_end_temp=[]
    for TMIN,TAVG,TMAX in dresults:
        start_end_temp_dict={}
        start_end_temp_dict["Min_Temp"]=TMIN
        start_end_temp_dict["Avg_Temp"]=TAVG
        start_end_temp_dict["Max_Temp"]=TMAX   
        start_end_temp.append(start_end_temp_dict)
    return jsonify(start_end_temp)



if __name__ == '__main__':
    app.run(debug=True)