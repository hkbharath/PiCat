#!/bin/bash
train_data="lenTrainLargeSet"
validate_data="lenValidationLargeSet"

main_train=33000
main_val=6600
special_train=10000
special_val=2000

for char_len in 1 2 3 4 5 6
do
    python3 generate.py --width 128 --height 64 --length $char_len --count $main_train --output-dir $train_data --symbols Symbolsets/symbols.txt
    python3 generate.py --width 128 --height 64 --length $char_len --count $special_train --output-dir $train_data  --symbols Symbolsets/special.txt
    python3 generate.py --width 128 --height 64 --length $char_len --count $main_val --output-dir $validate_data --symbols Symbolsets/symbols.txt
    python3 generate.py --width 128 --height 64 --length $char_len --count $special_val --output-dir $validate_data --symbols Symbolsets/special.txt
done
