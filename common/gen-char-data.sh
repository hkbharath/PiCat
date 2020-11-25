#!/bin/bash

train_data=$1
validate_data=$2
length=6
main_train=10000
main_val=2000
special_train=20000
special_val=4000

python3 generate.py --width 128 --height 64 --length $length --count $main_train --output-dir $train_data --symbols symbol_sets/symbols.txt
python3 generate.py --width 128 --height 64 --length $length --count $special_train --output-dir $train_data  --symbols symbol_sets/special.txt
python3 generate.py --width 128 --height 64 --length $length --count $main_val --output-dir $validate_data --symbols symbol_sets/symbols.txt
python3 generate.py --width 128 --height 64 --length $length --count $special_val --output-dir $validate_data --symbols symbol_sets/special.txt
