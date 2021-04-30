# NYCTaxiData

Few analytics problems solution on NYC taxi data. (Without Docker as of now)

## Setup SQL

The database dump from MySQL is exported and kept here.

```bash
SqlDump: Dump20210430.sql
```

## Usage

```python
#python NYCTaxiData_Task1.py 'year' 'month'

python NYCTaxiData_Task1.py "2019" "01"

```
This will take the data from table year and month wise and populate the required popular trip table.

## Database tables
``` bash
nyc_taxi_data (main taxi data)
taxi_zone_lookup (zone lookup)
nyc_popular_trips (output)
```

## Contributing
Lot of changes to be done in the current code.

