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


if __name__ == "__main__":
    app.run(debug=True)
