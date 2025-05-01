#!/bin/csh -f

source /usr/share/Modules/init/csh
set prompt = " "
#conda init
#conda activate tempest_extremes
module load geoclim/anaconda3/2024.10  
conda activate geoclim

set yrname = ("2021" "2022" "2023" "2024")
#set yrname = ("2019")

@ iyr = 1
@ len = $#yrname

cd /home/el2358/GEOCLIM/el2358/projects/tc_tracker/data_output
set data_in_dir = /home/el2358/GEOCLIM/el2358/projects/tc_tracker/era5_data_input
set dir2 = /home/el2358/GEOCLIM/el2358/projects/tc_tracker/data_output

while ($iyr <= $len)

	set year = $yrname[$iyr]
	echo $year
		
	#set h300file = $data_in_dir"h300/era5.geopotential.300."$year".nc"
	#set h500file = $data_in_dir"h500/era5.geopotential.500."$year".nc"
	set hfile = $data_in_dir"/era5.geopotential."$year".nc"
	set slpfile = $data_in_dir"/era5.mean_sea_level_pressure."$year".nc"
	set u10file = $data_in_dir"/era5.10m_u_component_of_wind."$year".nc"
	set v10file = $data_in_dir"/era5.10m_v_component_of_wind."$year".nc"

	DetectNodes \
		--in_data "$hfile;$slpfile;$u10file;$v10file"\
		--out "DN.ERA5.TC.$year.TEST.txt"\
		--searchbymin "msl" \
		--closedcontourcmd "msl,200.0,5.5,0;_DIFF(z(300hPa),z(500hPa)),-58.8,6.5,1.0" \
		--mergedist 6.0 \
		--outputcmd "msl,min,0;_VECMAG(u10,v10).max,2" \
		--latname "latitude" \
		--lonname "longitude" \

	@ iyr++
end
