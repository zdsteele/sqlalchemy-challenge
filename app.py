
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


@app.route("/")
def welcome():
    return (
        f"Welcome to Zach's SqlAlchemy Homework, here is a list of avalible routes"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def one():
    results = session.query(Measurement.date, Measurement.prcp).all()
    output = []
    for result in results:
       result = result._asdict()
       output.append(result)
    return jsonify(output)    
   

@app.route("/api/v1.0/stations")
def two():
    resultstwo = session.query(Measurement.station).all()
    outputtwo = []
    for resulttwo in resultstwo:
        resulttwo = resulttwo._asdict()
        outputtwo.append(resulttwo)
    return jsonify(outputtwo)

@app.route("/api/v1.0/tobs")
def three():
    resultsthree = session.query(Measurement.date, Measurement.tobs).limit(365)

    session.close()

    outputthree = [] 
    for resultthree in resultsthree:
        resultthree = resultthree._asdict()
        outputthree.append(resultthree)

    return jsonify(outputthree)


@app.route("/api/v1.0/<start>")

def four(start):
    session = Session(engine)
    start = '2012-02-28' 

    resultsfour = list(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()) 

    session.close()    

    return jsonify(resultsfour) 

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start,end):
    session = Session(engine)
    start = '2012-02-28'
    end = '2021-03-05'
  
    
    resultsfive = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    return jsonify(resultsfive)


if __name__ == "__main__":
    app.run(debug=True)