import numpy as np

import sqlalchemy
from sqlalchemy import engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    strDate = session.query(func.max(measurement.date)).first()[0]
    lastDate = dt.datetime.strptime(strDate, '%Y-%m-%d')
    prevYear = lastDate - dt.timedelta(366)

    all_prcp = []
    for date, prcp in results:
        prcp_dict ={}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(stations.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
            filter(measurement.date > prevYear).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start="%Y-%m-%d", end="%Y-%m-%d"):

    session = Session(engine)

    sel = [ func.min(measurement.tobs), 
       func.max(measurement.tobs), 
       func.avg(measurement.tobs)]

    results = session.query(*sel).filter(measurement.date,start, end).all()

    session.close()

    all_dates  = list(np.ravel(results))

    return jsonify(all_dates)

@app.route("/api/v1.0/temp/<start>")
def starts(start="%Y-%m-%d"):

    session = Session(engine)

    sel = [ func.min(measurement.tobs), 
       func.max(measurement.tobs), 
       func.avg(measurement.tobs)]

    results = session.query(*sel).filter(measurement.date >= start).all()
    
    return jsonify(results)


@app.route("/api/v1.0/temp/<start>/<end>")
def startend(start="%Y-%m-%d", end="%Y-%m-%d"):

    session = Session(engine)

    sel = [ func.min(measurement.tobs), 
       func.max(measurement.tobs), 
       func.avg(measurement.tobs)]

    results = session.query(*sel).filter(measurement.date>=start).filter(end>= measurement.date).all()

    session.close()

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
