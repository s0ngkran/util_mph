echo 
echo "step2..."
echo "get mph result"
echo

echo
echo "!!! do not forget to activate your python env"
echo

path=mph_keypoints.json.vr_poh_1k
out=mph_result.txt.vr_poh_1k_only_testing_set
gt_keypoint_path=../data_zip/poh_vr_1k/keypoints.json

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
