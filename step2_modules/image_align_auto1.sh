rescale-image-for-alignment --input "/data/proxy/*.tif" --atlas-file /reference/P56_Atlas.tif --output /data/proxy_whole.tif --flip-z --flip-y

sitk-align --moving-file /data/proxy_whole.tif --fixed-file /reference/P56_Atlas.tif --fixed-point-file /reference/P56_points.json --xyz --alignment-point-file /data/proxy_whole_alignment.json

nuggt-align --port 8999 --reference-image /reference/P56_Atlas.tif --moving-image /data/proxy_whole.tif --points /data/proxy_whole_alignment.json
