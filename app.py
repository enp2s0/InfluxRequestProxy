from flask import Flask, request
from influxdb import InfluxDBClient

# Configuration file is actually a python source file.
import config

# Create some necessary objects.
client = InfluxDBClient(host = config.INFLUX_HOST, port = config.INFLUX_PORT, database = config.INFLUX_DB)
app = Flask(__name__)

@app.route("/ingest")
def ingest():
	data = {}
	for arg in request.args:
		# Get the parameter string.
		val = request.args[arg]

		# Skip this parameter if it's in the placeholder list.
		if val in config.NULL_PLACEHOLDERS:
			continue

		# Try to convert the value to a float. If it fails, convert to a string
		try:
			fmt_val = float(val)
		except ValueError:
			fmt_val = val

		# Add this value to the list of datapoints to push
		data.update({arg: fmt_val})

	# Assemble a proper InfluxDB frame.
	influx_data = {}
	influx_data["measurement"] = config.INFLUX_MEASUREMENT
	influx_data["tags"] = {}
	influx_data["fields"] = data
	if_output = [influx_data]

	if config.DEBUG_ENABLE:
		print(if_output)

	# Actually write the points.
	client.write_points(if_output)

	# Return a dummy success value to satisfy Flask. Flask will handle returning errors if the code above hits an unhandled exception.
	return("200 OK")

# Run the Flask app on startup.
app.run(debug = config.DEBUG_ENABLE, host = config.PROXY_ADDR, port = config.PROXY_PORT)
