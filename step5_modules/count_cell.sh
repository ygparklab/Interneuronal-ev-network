# Transform maxima into jason coordinates
echo "Starting the cell counting process!" | lolcat
echo "Transforming maxima points into blobs. You may want to enter your password..." | lolcat
###detect-blobs###
	#--source <source-expr> - source-expr = GLOB expression for collecting .tif files
	#--output <coords-file> - name of the output file; json-encoded list of lists where inner 		list has xyz coordinates of a putative cell in that order
	#--dog-low <dog-low-sigma-z> - stdev of Gaussian used for smoothing the foreground
	#--dog-low-xy, --dog-low-z = same
	#--dog-high <dog-high-sigma> - stdev of Gaussian used for smoothing the background 		(background subtracted from the smoothed foreground to get diff in Gaussians (dog)
	#--threshold <threshold> - abs cutoff for peak finding. Any peak must have a value above 		this threshold in the diff of gaussians
	#--min-distance <min-distance> - min dist in voxels between adj peaks. peak with higher 		intensity chosen if two are within the distance. larger = computationally expensive
	#--min-distance--xy, --min-distance-z = same
	#--block-size-xy <block-size> - size of the processing block in xy direction; block size 		(block-size-xy*block-size-xy*block-size-z)*core no.*8 << memory size
	#--block-size-z = same
	#--padding-xy - amount of padding on xy sides of block, large enough for Gaussian to be 		computed
	#--padding-z = same
sudo detect-blobs --source "Ex_561_Em_600_total_detection/Img_Z*.tif" --output blobs_.json --threshold 0 --min-distance 5 | lolcat
echo "Done with transforming maxima into blobs, proceeding to counting the soma..." | lolcat

# Count point in regions
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_whole_lvl4.csv --level 4 --xyz  | lolcat
echo "|>         | 8% done!"  | lolcat
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_whole_lvl5.csv --level 5 --xyz  | lolcat
echo "|>>        | 16% done!"  | lolcat
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_whole_lvl6.csv --level 6 --xyz
echo "|>>        | 24% done!"  | lolcat
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_whole_lvl7.csv --level 7 --xyz  | lolcat
echo "|>>>       | 32% done!"  | lolcat
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_whole_lvl8.csv --level 8 --xyz  | lolcat
echo "|>>>>>     | 48% done!"  | lolcat
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_whole_lvl9.csv --level 9 --xyz  | lolcat
echo "|>>>>>>    | 56% done!"  | lolcat
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation_whole_RH.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_rh_lvl4.csv --level 4 --xyz  | lolcat
echo "|>>>>>>    | 64% done!"  | lolcat
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation_whole_RH.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_rh_lvl5.csv --level 5 --xyz  | lolcat
echo "|>>>>>>>   | 72% done!"  | lolcat
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation_whole_RH.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_rh_lvl6.csv --level 6 --xyz  | lolcat
echo "|>>>>>>>>  | 80% done!"  | lolcat
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation_whole_RH.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_rh_lvl7.csv --level 7 --xyz  | lolcat
echo "|>>>>>>>>> | 88% done!" | lolcat
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation_whole_RH.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_rh_lvl8.csv --level 8 --xyz  | lolcat
echo "|>>>>>>>>> | 94% done!" | lolcat
count-points-in-region --points blobs_.json --alignment native_whole_alignment.json --reference-segmentation /atlas/CCFv3/P56_Annotation_whole_RH.tif --brain-regions-csv /atlas/allen-mouse-brain-atlas/AllBrainRegions.csv --output  cell_count_rh_lvl9.csv --level 9 --xyz  | lolcat
echo "|>>>>>>>>>>| 100% done!" | lolcat
echo "Process Complete!" | lolcat
