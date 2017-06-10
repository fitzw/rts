# rts
Real time public transportation travel planner

* n: records per file
* stop_id: id of the stop from the file 
* type: transportation type, Bus by default. 
 See[stops.txt](https://github.com/fitzw/rts/blob/master/MBTA_GTFS/stops.txt)
* route_n: transportation's route #, 39 by default
```
$ python data_collector.py 

Please enter parameters in format of: n, stop_id, type, route_n =>

360, 175, Bus, 39
```
