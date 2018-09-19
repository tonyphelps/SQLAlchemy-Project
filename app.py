import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
# Create our session (link) from Python to the DB
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the dates and temperature observations from the last year."""
    # Query for Precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date <= "2017-08-23", Measurement.date >='2016-08-23').all()

    precipitation = [results]

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations from dataset"""
    # Query all passengers
    results = session.query(Station.name, Station.station).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = [results]
  
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the dates and temperature observations from the last year."""
    # Query for Temperature
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date <= "2017-08-23", Measurement.date >='2016-08-23').all()

    # Convert query to Dictionary
    temp_list = []
    for result in results:
        temp_dict = {}
        temp_dict['Date'] = result[0]
        temp_dict['Tobs'] = result[1]
        temp_list.append(temp_dict)

    return jsonify(temp_list)

@app.route('/api/v1.0/<date>/')
def start_date(date):
    """Return the min temp, avg temp, and max temp for the date"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= date).all()

    # creates JSONified list of dictionaries
    start_list = []
    for result in results:
        start_dict = {}
        start_dict['Start Date'] = date
        start_dict['End Date'] = '2017-08-23'
        start_dict['TMin'] = float(result[0])
        start_dict['TAvg'] = float(result[1])
        start_dict['TMax'] = float(result[2])
        
        start_list.append(start_dict)

    return jsonify(start_list)

@app.route('/api/v1.0/<start_date>/<end_date>/')
def date_range(start_date, end_date):
    """Return the min, avg, & max temp over a specific date range"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    # creates JSONified list of dictionaries
    range_list = []
    for result in results:
        range_dict = {}
        range_dict["Start Date"] = start_date
        range_dict["End Date"] = end_date
        range_dict["TMin"] = float(result[0])
        range_dict["TAvg"] = float(result[1])
        range_dict["TMax"] = float(result[2])
       
        range_list.append(range_dict)
    return jsonify(range_list)



if __name__ == '__main__':
    app.run(debug=True)
