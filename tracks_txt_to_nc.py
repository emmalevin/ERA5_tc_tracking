

import datetime, glob, sys, os.path
import numpy as np, xarray as xr, pandas as pd

#def tc_read(ifile, n_storms_bound=None, hour24=True):
if True:

    year_list = ['2019','2020','2021','2022','2023','2024']

    for iyear in year_list:  
        ifile = 'tracks.ERA5.TC.{}.TEST.txt'.format(iyear)
        n_storms_bound = None
        '''Extract TC information from txt file and convert to Dataset.

        Input: ifile, tc txt file, e.g. /tigress/wenchang/MODEL_OUT/CTL1860_noleap_tigercpu_intelmpi_18_576PE/analysis_lmh/cyclones_gav_ro110_1C_330k/atmos_11_11/Harris.TC/lmh_TCtrack_ts_4x.dat.warm.h29_25.TS.world.20110101-20120101.txt
        Return: xr.Dataset
        '''
        # e.g. ifile = '/tigress/wenchang/MODEL_OUT/CTL1860_noleap_tigercpu_intelmpi_18_576PE/analysis_lmh/cyclones_gav_ro110_1C_330k/atmos_11_11/Harris.TC/lmh_TCtrack_ts_4x.dat.warm.h29_25.TS.world.20110101-20120101.txt'


        # columns of the txt file
        names = ('test1', 'test2', 'lon', 'lat', 'slp', 'windmax', 'year', 'month', 'day', 'hour')

        # use pandas to read the txt file
        df = pd.read_csv(ifile, sep='\s+', names=names)
        L = np.array(['start' in t for t in df.test1]) # select lines of summary
        isummaries = df.index[L]
        istarts = isummaries + 1 # indices of storm starts
        iends = np.hstack( ( isummaries[1:]-1, df.index[-1])) # indices of storm ends

        # length of the storm dimension
        if n_storms_bound is None:
            n_storms_bound = L.sum()

        # save each variable associated the storms into a 2D ndarray
        shape = (n_storms_bound, 120) # n_storms, n_steps(6-hourly)
        lat = np.zeros(shape) + np.nan
        lon = np.zeros(shape) + np.nan
        windmax = np.zeros(shape) + np.nan
        slp = np.zeros(shape) + np.nan
        year = np.zeros(shape) + np.nan
        month = np.zeros(shape) + np.nan
        day = np.zeros(shape) + np.nan
        hour = np.zeros(shape) + np.nan
        # loop over all storms
        for i, (istart, iend) in enumerate(zip(istarts, iends)):
            nsteps = min(iend + 1 - istart, shape[1]) # number of steps along the track of a storm, sometimes greater than the specified number of steps shape[1]
            ilocs = slice(istart, istart+nsteps)
            lat[i, :nsteps] = df.iloc[ilocs]['lat']
            lon[i, :nsteps] = df.iloc[ilocs]['lon']
            windmax[i, :nsteps] = df.iloc[ilocs]['windmax']
            slp[i, :nsteps] = df.iloc[ilocs]['slp']
            year[i, :nsteps] = df.iloc[ilocs]['year']
            month[i, :nsteps] = df.iloc[ilocs]['month']
            day[i, :nsteps] = df.iloc[ilocs]['day']
            hour[i, :nsteps] = df.iloc[ilocs]['hour']


        # wrap ndarray into DataArray
        dims = ('storm', 'stage')
        storm = xr.DataArray(np.arange(1, shape[0]+1))
        stage = xr.DataArray(np.arange(shape[1])*6,
                            attrs={'units': 'hours from genesis'})
        coords = [storm, stage]
        lat = xr.DataArray(lat, dims=dims, coords=coords,
                          attrs={'long_name': 'latitude',
                                'units': 'degree north'})
        lon = xr.DataArray(lon, dims=dims, coords=coords,
                          attrs={'long_name': 'longitude',
                                'units': 'degree east'})
        windmax = xr.DataArray(windmax, dims=dims, coords=coords,
                          attrs={'long_name': 'max wind speed',
                                'units': 'm/s'})
        slp = xr.DataArray(slp, dims=dims, coords=coords,
                          attrs={'long_name': 'sea level pressure',
                                'units': 'hPa'})
        year = xr.DataArray(year, dims=dims, coords=coords)                  
        month = xr.DataArray(month, dims=dims, coords=coords)
        day = xr.DataArray(day, dims=dims, coords=coords)
        hour = xr.DataArray(hour, dims=dims, coords=coords)

        # wrap DataArray into Dataset
        ds = xr.Dataset(dict(lat=lat, lon=lon,
                             windmax=windmax, slp=slp, year=year,
                             month=month, day=day, hour=hour))

        #return ds
        ds.to_netcdf('test{}.nc'.format(iyear))
        print(iyear)
