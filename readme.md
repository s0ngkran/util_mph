# to get result of MPH

## steps to run
1. edit config.json to have the correct img_dir
2. edit read_data() 
3. run step1_get_mph_keypoints.sh
4. run step2_get_mph_result.sh

## more detail

### config

you have to edit config.json
working dir is mph_module/*
```json
{
  "img_dir": "../dataset/images/",
}
```
and edit read_data() to return a list of <class MPHInput>

### ground truth

gt positions of Thai Finger Spelling
```txt
  5 7 9 []
  | | | |
  | | | |
  4 6 8 10
  
2    3
  1
     0
```

### step1
output = mph_keypoints.json

### step2
output = mph_result.sh

