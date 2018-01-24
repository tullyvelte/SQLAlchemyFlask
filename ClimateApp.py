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

# Save references to the invoices and invoice_items tables
Measurements = Base.classes.measurements
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/start"
        f"/api/v1.0/start/end"

    )

@app.route("/api/v1.0/precipitation")
def get_precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = datetime.date(2017, 8, 23) - datetime.timedelta(days=365)
    rain = (session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date > last_year)
        .order_by(Measurement.date)
        .all())
    
    rain_totals = []
    for rain in rain_totals:
        row = {}
        row['date'] = rain[0]
        rain['prcp'] = rain[1]
        rain_totals.append(row)
        
    return jsonify(rain_totals)

@app.route("/api/v1.0/stations")
def get_stations():
    station_query =(session.query(Station.name, Station.station) 
    .all())
    
    station_list =[]
    sd = {}
    for row in station_query:
        sd['station code']=row[0]
        sd['station name']=row[1]
        station_list.append(sd)
        
    return json.dumps(json_list, separators=(',',':'))

@app.route("/api/v1.0/tobs")
def get_prev_temp():
    last_date = session.query(Measurement.date, Measurement.tobs)
    last_year = datetime.date(2017, 8, 23) - datetime.timedelta(days=365)
    prev_temp_query = (session
            .query(Measurement.tobs, Measurement.date, Measurement.station)
            .filter(Measurement.date > last_year)
            .all())
    
    prev_list =[]
    pd = {}
    for row in prev_temp_query:
        pd['station code']=row[2]
        pd['date']=row[1]
        pd['temp']=row[0]
        prev_list.append(pd)
        
    return json.dumps(json_list, separators=(',',':'))

@app.route("/api/v1.0/start")
@app.route("/api/v1.0/start/end")
def get_start_end(start, end="2017-31-12"):
    start_date =  datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    result = calc_temp(start_date, end_date)
    dates = {}
    dates['Minimum Temp'] = result[0][0]
    dates['Maximum Temp'] = result[0][1]
    dates['Average Temp'] = result[0][2]
    
    return jsonify(mydict)

if __name__ == '__main__':
    app.run(debug=True)