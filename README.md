## InfluxRequestProxy

Push data into InfluxDB using HTTP GET requests.

#### Dependencies

`InfluxRequestProxy` depends on `Python 3`, `Flask`, and `InfluxDBClient`.

#### Usage

Rename `config.py.example` to `config.py` and edit appropriately. Launch the proxy with `python3 app.py`.

#### FAQ/Notes

**Why wouldn't you just use the InfluxDB REST API?**

You should use the API if possible. This proxy was written to allow an embedded weather station controller that could *only* make GET requests to push it's data into InfluxDB. If you have the ability to make POST requests, you can (and should) use the API.

**How should I structure my GET requests?**

The format is extremely simple:

`<proxy address>:<proxy port>/ingest?field1=val1&field2=val2&fieldX=valX`

**How does the proxy know what data type to use?**

It tries to use `float`, and if that fails it uses `string`. It is an incredibly stupid method but also extremely simple and it works for the single use case I have for this proxy. If you need better handling of data types open an issue and I'll see if I can figure something out.

**What about tags or multiple measurements?**

Neither tags nor multiple measurements are currently supported. As mentioned above, I wrote this with a very specific use case that does not need these features: a single controller pushing a few values (temperature, humidity, pressure, wind speed) every 5 seconds.

