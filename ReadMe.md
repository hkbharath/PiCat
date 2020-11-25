## Contents

1. Padding Model Approach -> explained in `padding_model` folder. 
2. Two Model Approach -> explained in `two_model` folder.
3. `common` folder contains the `generate.py` and scripts used to generate the training sets.
4. `misc_test` folder contains a sample code used to check the effect of noise cancellation that we tried.
5. `setup/package.sh` can be used to push the newly trained to the `PiCatClient` repository, form where the model is being pulled in to the pi.  
    `$ bash package.sh <Model Dir> <Target Dir>`  
      
    Traget directory should be the valid git reposiroty of `PiCatClient` -> https://github.com/hkbharath/PiCatClient.git. SSH keys should be setup in the git account to use this script to update the `PiCatClient` package.

6. `setup/classify.sh` should be run in pi, to create the environment and to start the classification of new captcha images. This script also updates the models in th pi before starting the classification step. And handles interruptions in any stage from setting environment to running classification on the image.  
    `$ bash classify.sh <Captcha Dir>`

-----------------------------------------