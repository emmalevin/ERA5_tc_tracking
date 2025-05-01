#!/bin/csh
#conda init
#conda activate tempest_extremes

source /usr/share/Modules/init/csh
set prompt = " "
#conda init
#conda activate tempest_extremes
module load geoclim/anaconda3/2024.10
conda activate geoclim

set dir = /home/el2358/GEOCLIM/el2358/projects/tc_tracker
cd $dir/stitch_data_output
 
set yrname = ("2019" "2020" "2021" "2022" "2023" "2024")
#set yrname = ("2018")

@ len = $#yrname
@ iyr = 1
#@ len = 10

while ($iyr <= $len)
	set year = $yrname[$iyr]
	echo year

		set dnfile = /home/el2358/GEOCLIM/el2358/projects/tc_tracker/data_output/DN.ERA5.TC.$year.TEST.txt
		set outfile = ./tracks.ERA5.TC.$year.TEST.txt

		StitchNodes \
			--in "$dnfile" \
			--out "$outfile" \
			--in_fmt "lon,lat,slp,wind10m" \
			--range 8.0 \
			--mintime "54h" \
			--maxgap "24h" \
			--threshold "wind10m,>=,10.0,10;lat,<=,50.0,10;lat,>=,-50.0,10"
	@ iyr++
end

# Note: zs here is geopotential (geopotential height * g), therefore, I use a more strict criteria
# geopotential < 1470 m^2/s^2 --> is equivalent to geopotential height < 150 m
# 1470 = 150 * 9.8
