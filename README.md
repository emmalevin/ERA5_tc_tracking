# ERA5_tc_tracking
Tracking Tropical Cyclones (TCs: 2018-2024) using 6-hourly ERA5 reanalysis data

- [ERA5 data](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview)
- [TempestExtremes tracking algorithm](https://climate.ucdavis.edu/tempestextremes.php)
- TC tracking example [here](https://gmd.copernicus.org/articles/14/5023/2021/) in section 3.2

Necessary 6-hourly inputs:
1. Sea level pressure (looking for local minima in sea level pressure to identify a potential cyclone)
2. Geopotential at 300 and 500 hPa or temperature at 400 hPa (to detect a [warm core](https://journals.ametsoc.org/view/journals/mwre/147/3/mwr-d-18-0276.1.xml#:~:text=The%20typical%20warm%2Dcore%20height%20is%20at%20the,hPa%20(~14%20km)%20for%20category%205%20hurricanes.) of the storm, differentiating the TC from a typical mid-latitude cyclone)
3.  10m u-wind and 10m v-wind (not used for TC candidate, but we calculate maximum wind speed of the storm to study the storm's intensity evolution and to stitch together storms)

Files:
- era5_tracks_data_modify.ipynb: ensure the ERA5 data is compatible with the TempestExtremes algorithm
- DN.ERA5_TC_TEST.csh: detecting potential TC candidate points (must be local minima in sea level pressure and have a warm core)
- SN.ERA5_TC_TEST.csh: stitching together individual storms (storms must last at least 54 hours, have maximum wind speeds exceeding 10 m/s for at least 10 time slices, and lie between 50S-50N for at least 10 time slices)
- tracks_txt_to_nc.py: converts tc track txt file to a netcdf file that is easier for analysis
- era5_tc_tracks_2018_2024.nc: netcdf file of TC tracks




