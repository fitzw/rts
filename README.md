# rts
Real time public transportation travel planner

## Data collection
* n: # of records per data file.
* stop_id: id of stop, see [stops.txt](https://github.com/fitzw/rts/blob/master/MBTA_GTFS/stops.txt)
* type: type of transportation, Bus for instance.
* route_n: the route # of given transportation, 39 for instance.
```
$ python data_collector.py 

Please enter parameters in format of: n, stop_id, type, route_n =>

1200, 175, Bus, 39
```