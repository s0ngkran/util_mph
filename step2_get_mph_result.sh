echo 
echo "step2..."
echo "get mph result"
echo

echo
echo "!!! do not forget to activate your python env"
echo

python main.py ori mph_keypoints.json > mph_result.txt;
python main.py h1 mph_keypoints.json>> mph_result.txt;
python main.py h2 mph_keypoints.json>> mph_result.txt;
python main.py angle mph_keypoints.json>> mph_result.txt;

echo 'writed to mph_result.txt'
