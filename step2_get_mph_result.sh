echo 
echo "step2..."
echo "get mph result"
echo

echo
echo "!!! do not forget to activate your python env"
echo

path=mph_keypoints.json.poh_plain_black
out=mph_result.txt.poh_plain_black
gt_keypoint_path=../data_zip/poh_plain_vs_natural/processed/poh_black_testing.json

echo "using $path"
echo "output $out"
echo

python main.py ori $path $gt_keypoint_path > $out;
python main.py h1 $path $gt_keypoint_path >> $out;
python main.py h2 $path $gt_keypoint_path>> $out;
python main.py angle $path $gt_keypoint_path>> $out;
python main.py angleE $path $gt_keypoint_path>> $out;
python main.py dist $path $gt_keypoint_path>> $out;
python main.py depth $path $gt_keypoint_path>> $out;
python main.py handedness $path $gt_keypoint_path>> $out;
python main.py paper $path $gt_keypoint_path>> $out;

echo "writed to ${out}"
