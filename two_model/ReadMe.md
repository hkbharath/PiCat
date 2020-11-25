## Training the character recognition model
Use the training and validation captcha images containging fixed length captchas to train this model.

`python train_char.py --width 128 --height 64 --length 6 --batch-size 64 --train-dataset <Train set dir> --validate-dataset <Train set dir> --output-model-name <Character Model Output Directory> --epochs=15 --symbols <Symbol set file>`  

-----------------------------------------

## Training the length recognition model
Use the training and validation captcha images containging variable length captchas to train this model.

`python train_length.py --width 128 --height 64 --length 6 --batch-size 64 --train-dataset <Train set dir> --validate-dataset <Train set dir> --output-model-name <Length Model Output Directory> --epochs=15 --symbols <Symbol set file>`

-----------------------------------------

## Monitoring the training

`tensorboard --logdir < Model Output Directory >/fit`

## Testing the classifications locally
Before moving the model to the `PiCatClient` repository, we can test the model with following command locally.

`python classify_test.py --model-name <Character Model Output Directory> --len-model-name <Length Model Output Directory> --captcha-dir <Classify Image Dir> --output <Prediction output file> --symbols <Symbol set>`

-----------------------------------------