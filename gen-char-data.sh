#!/bin/bash

train_data="charTrainSet"
validate_data="charValidationSet"
length=6
# main_train=10000
# main_val=2000
# special_train=20000
# special_val=4000

main_train=100
main_val=20
special_train=200
special_val=40

python3 generate.py --width 128 --height 64 --length $length --count $main_train --output-dir $train_data --symbols Symbolsets/symbols.txt
python3 generate.py --width 128 --height 64 --length $length --count $special_train --output-dir $train_data  --symbols Symbolsets/special.txt
python3 generate.py --width 128 --height 64 --length $length --count $main_val --output-dir $validate_data --symbols Symbolsets/symbols.txt
python3 generate.py --width 128 --height 64 --length $length --count $special_val --output-dir $validate_data --symbols Symbolsets/special.txt
