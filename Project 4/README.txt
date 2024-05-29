## Data Cleansing

* **Dropped rows** where key columns (`MMSI`, `Latitude`, `Longitude`, `timestamp`) are null.
* **Removed duplicates** based on `MMSI`, `Latitude`, `Longitude`, and `timestamp`.
* **Filtered out** invalid latitude and longitude values (Latitude: -90 to 90, Longitude: -180 to 180).
* **Excluded rows** with unrealistic speeds (greater than 107 km/h) based on calculated speed. Threshold was selected based on the current quickest ship - HSC Francisco.

## Longest Distance Travelled

* Using the `geopy` module, we calculated the distance traveled between consecutive points for each vessel. This step required handling missing values carefully to avoid calculation errors.
* We identified the vessel with MMSI `219133000` as having traveled the longest distance, covering `790 km`.
