# to get result of MPH
run two steps
- step1_get_mph_keypoints.sh
- step2_get_mph_result.sh

## config
you can config.json
working dir is mph_module/*
```json
{
  "img_dir": "../dataset/images/",
  "gt_json": "../dataset/gt.json"
}
```

## gt_json
```json
{
  "0": {
    "img_path": "001.jpg",
    "gt": 1, 
  },
  ...
}
```

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


## step1
generate mph_keypoints.json

## step2
generate mph_result.sh

