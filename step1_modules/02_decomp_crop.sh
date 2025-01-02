echo "Optimizing the first channel..." | lolcat

tiffcrop  -U px -m 108,792,388,373 -es -c none Ex_488_Em_525_stitched/*.tif source/Ex_488_Em_525/img_Z.tif
cd source/Ex_488_Em_525/
echo "Renaming files..."
rename 's/(\d+)(?=.*\.)/sprintf("%04d",$1)/eg' *
cd ../../

echo "Optimizing the second channel..." | lolcat

tiffcrop  -U px -m 108,792,388,373 -es -c none Ex_561_Em_600_stitched/*.tif source/Ex_561_Em_600/img_Z.tif
cd source/Ex_561_Em_600/
echo "Renaming files..."
rename 's/(\d+)(?=.*\.)/sprintf("%04d",$1)/eg' *
cd ../../

echo "Optimizing the third channel..." | lolcat
tiffcrop  -U px -m 108,792,388,373 -es -c none Ex_647_Em_680_stitched/*.tif source/Ex_647_Em_680/img_Z.tif
cd source/Ex_647_Em_680/
echo "Renaming files..."
rename 's/(\d+)(?=.*\.)/sprintf("%04d",$1)/eg' *
cd ../../

echo "Done. Go to '/source'. I'm out!" | lolcat
