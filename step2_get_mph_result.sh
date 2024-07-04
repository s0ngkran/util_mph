echo 
echo "step2..."
echo "get mph result"
echo

echo
echo "!!! do not forget to activate your python env"
echo

python main.py ori > mph_result.sh 
python main.py h1 >> mph_result.sh 
python main.py h2 >> mph_result.sh 
