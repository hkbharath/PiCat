## Training the model
Use the training and validation captcha images containging variable length captchas to train this model.

`python train.py --width 128 --height 64 --length 6 --batch-size 64 --train-dataset <Train set dir> --validate-dataset <Train set dir> --output-model-name <Model Output Directory> --epochs=15 --symbols <Symbol set file>` 

-----------------------------------------

## Monitoring the training
`tensorboard --logdir < Model Output Directory >/fit`

-----------------------------------------

## Trained model with 98% accuracy
`final_model` contains the tensorflow model and the `.tflite` model which was trained with this approach. This can used to classfify the variable length captchas.

-----------------------------------------

## Testing the classifications locally
Before moving the model to the `PiCatClient` repository, we can test the model with following command locally.

`python classify_test.py --model-name <Model Output Directory> --captcha-dir <Classify Image Dir> --output <Prediction output file> --symbols <Symbol set>`

-----------------------------------------
