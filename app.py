# Import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


###### DATABASE SETUP ######
# Establish connection to database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect database into a new model
Base = automap_base()

# Reflect the tables into clases
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


###### FLASK SETUP ######
app = Flask(__name__)


###### FLASK ROUTES ######

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f'<a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br/>'
        f'<a href="/api/v1.0/stations">/api/v1.0/stations</a><br/>'
        f'<a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br/>'          
        f"/api/v1.0/start_date <-- <i>Enter date as mmddyyyy</i><br/>"
        f"/api/v1.0/start_date/end_date <-- <i>Enter dates as mmddyyyy</i>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    """Precipitation measurments by date"""

    session = Session(bind=engine)

    prcp_query_results = (session.query(Measurement.date, Measurement.prcp)
              .filter(Measurement.date >= '2016-08-23').all())

    session.close()
    
    prcp_query_output = []
    for date, prcp in prcp_query_results:
        result_dict = {}
        result_dict["date"] = date
        result_dict["prcp"] = prcp
        prcp_query_output.append(result_dict)

    return jsonify(prcp_query_output)

@app.route("/api/v1.0/stations")
def stations():
    """Weather station list"""

    session = Session(bind=engine)

    station_list_query_results = session.query(Station.id, Station.station, Station.name).all()
    
    session.close()

    station_list_output = []
    for id, station, name in station_list_query_results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_list_output.append(station_dict)

    return jsonify(station_list_output)

@app.route("/api/v1.0/tobs")
def tobs():
    """Place Holder"""

    session = Session(bind=engine)

    prcp_query_results = (session.query(Measurement.tobs)
              .filter(Measurement.date >= '2016-08-23')
              .filter(Measurement.station == "USC00519281").all())

    session.close()

    results = list(np.ravel(prcp_query_results))
    
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start(start=None):
    """Place Holder"""

    session = Session(bind=engine)

    start = dt.datetime.strptime(start, "%m%d%Y")

    start_query_results = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
              .filter(Measurement.date >= start).all())

    session.close()

    results = list(np.ravel(start_query_results))
    
    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    """Place Holder"""

    session = Session(bind=engine)

    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    start_end_query_results = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
              .filter(Measurement.date >= start)
              .filter(Measurement.date <= end).all())


    session.close()

    results = list(np.ravel(start_end_query_results))
    
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)