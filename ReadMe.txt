Note: This folder "PycharmProjects/SCP2" is the project root folder. Change this accordingly.
Setup GPU access with steps from: http://support.scss.tcd.ie/index.php/SCSS_GPU_Resources


****** Generate dataset for training length ******
# change necessary parameters if required
./gen-len-data.sh


****** Generate dataset for training character ******
# change necessary parameters if required
./gen-char-data.sh


****** Training the Models for characters ******
ssh <uname>@slurm-master.scss.tcd.ie
./register_job.sh python PycharmProjects/SCP2/train_char.py --width 128 --height 64 --length 6 --batch-size 64 --train-dataset PycharmProjects/SCP2/charTrainSet --validate-dataset PycharmProjects/SCP2/charValidationSet/ --output-model-name PycharmProjects/SCP2/Models/testChar --epochs=50 --symbols PycharmProjects/SCP2/Symbolsets/symbols.txt

****** Training the Models for length ******
ssh <uname>@slurm-master.scss.tcd.ie
./register_job.sh python PycharmProjects/SCP2/train_length.py --width 128 --height 64 --length 6 --batch-size 64 --train-dataset PycharmProjects/SCP2/lenTrainSet --validate-dataset PycharmProjects/SCP2/lenValidationSet/ --output-model-name PycharmProjects/SCP2/Models/testLen --epochs=50 --symbols PycharmProjects/SCP2/Symbolsets/symbols.txt


****** Starting Tensorboard ******
source /opt/conda/etc/profile.d/conda.sh
conda activate tf-gpu
cd PycharmProjects/SCP2/Models/<ModelName>/
tensorboard --logdir .
