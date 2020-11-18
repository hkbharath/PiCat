#!/bin/bash

train_data="charTrainSet"
validate_data="charValidationSet"
length=6
main_train=200000
main_val=40000
special_train=60000
special_val=12000

python3 generate.py --width 128 --height 64 --length $length --count $main_train --output-dir $train_data --symbols Symbolsets/symbols.txt
python3 generate.py --width 128 --height 64 --length $length --count $special_train --output-dir $train_data  --symbols Symbolsets/special.txt
python3 generate.py --width 128 --height 64 --length $length --count $main_val --output-dir $validate_data --symbols Symbolsets/symbols.txt
python3 generate.py --width 128 --height 64 --length $length --count $special_val --output-dir $validate_data --symbols Symbolsets/special.txt
