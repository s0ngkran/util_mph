echo 
echo "step2..."
echo "get mph result"
echo

echo
echo "!!! do not forget to activate your python env"
echo

path=mph_keypoints.json.vr_poh_1k
out=mph_result.txt.vr_poh_1k_only_testing_set

echo "using $path"
echo "output $out"

python main.py ori $path > $out;
python main.py h1 $path >> $out;
python main.py h2 $path >> $out;
python main.py angle $path >> $out;
python main.py angleE $path >> $out;
python main.py dist $path >> $out;
python main.py depth $path >> $out;
python main.py handedness $path >> $out;

echo "writed to ${out}"
