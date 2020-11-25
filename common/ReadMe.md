## Generate test/train data with variable length for traing padding model approach
-----------------------------------------
This script will create around 250k captcha images with 200K generated with all symbol set and 50K generated with special or confusing characters. And equal number of 1-6 length captcha images are generated.

`./gen-len-data.sh <Train Set Dir> <Test Set Dir>`

## Generate test/train data with fixed length captcha for traing two model approach
-----------------------------------------
This script creates fixed length captchas, which can be used to train the character recognition model in two model approach.

`./gen-char-data.sh <Train Set Dir> <Test Set Dir>`

## Python script to generate the captchas
-----------------------------------------
Above scripts use the `generate.py` to generate the captcha.

`python generate.py --width 128 --height 64 --length 6 --count <Img Count> --output-dir <image output dir> --symbols symbol_sets/symbols.txt`