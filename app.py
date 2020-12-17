from flask import Flask, request
from influxdb import InfluxDBClient
import pprint

client = InfluxDBClient(host = "status.net.lan", port = 8086, database = "weatherdata")
app = Flask(__name__)
pp = pprint.PrettyPrinter(indent = 4)

@app.route("/ingest")
def ingest():
	data = {}
	for arg in request.args:
		val = request.args[arg]
		if val == "NULL":
			continue
		data.update({arg: float(request.args[arg])})

	influx_data = {}
	influx_data["measurement"] = "meteobridge"
	influx_data["tags"] = {}
	influx_data["fields"] = data
	if_output = [influx_data]

	pp.pprint(if_output)
	client.write_points(if_output)

	return("200")

app.run(debug = False, host = "0.0.0.0", port = 8080)
