#!/bin/sh

usage(){
    echo "Invalid Arguments!!"
    echo "Usage: ./classify.sh <Captcha dir>"
}
vm_creation(){
	python3 -m venv $VENV_NAME
	if [ $? == 0 ]
	then
		echo "venv_created" >| $STATUS_FILE
	fi
	cloning
}	
cloning(){
	source ./$VENV_NAME/bin/activate
	if [ -d "$GIT_REP" ]
	then 
		rm -rf $GIT_REP
	fi
	git clone $GIT_REP
	if [ $? == 0 ]
	then
		echo "clone" >| $STATUS_FILE
	fi
	cd $GIT_DIR
	dependency
}	

update(){
	source ./$VENV_NAME/bin/activate
	cd $GIT_DIR
	git pull
	rm predictions.txt
	if [ $? == 0 ]
	then
		echo "update" >| ../$STATUS_FILE
	fi
	dependency
}
dependency(){
	pip install dependencies/linux_armv71/*.whl
	if [ $? == 0 ]
	then
		echo "todo_classify" >| ../$STATUS_FILE
	fi
	classify_go
}

classify_go(){
	python classify.py --model-name model --captcha-dir $CAPTCHA_DIR --output predictions.txt --symbols symbols.txt
	if [ $? == 0 ]
	then
		rm ../$STATUS_FILE
	fi
}


if [[ $# -lt 1 ]]
then
    usage
    exit 1
fi

GIT_REP="https://github.com/hkbharath/PiCatClient.git"
VENV_NAME="new_env"
BASE_FOLDER="base_folder_test0"
GIT_DIR="PiCatClient"
CAPTCHA_DIR=$1
STATE="intialize"
STATUS_FILE="status.txt"


if [ ! -d "$BASE_FOLDER" ] 
then
	mkdir $BASE_FOLDER
	cd $BASE_FOLDER
	echo "bf_created" >| $STATUS_FILE

	if [ -e $STATUS_FILE ]
	then 
		STATE=$(<$STATUS_FILE)
		if [ $STATE == "bf_created" ]
		then
			vm_creation
		fi
	fi
else
	cd $BASE_FOLDER
	if [ -e $STATUS_FILE ]
	then 
		STATE=$(<$STATUS_FILE)

		if [ $STATE == "update" ]
		then
			source ./$VENV_NAME/bin/activate
			cd $GIT_DIR
			depedency

		elif [ $STATE == "todo_classify" ]
		then
			source ./$VENV_NAME/bin/activate
			cd $GIT_DIR
			classify_go
		elif [ $STATE == "bf_created" ]
		then
			vm_creation

		elif [ $STATE == "venv_created" ]
		then
			 cloning

		elif [ $STATE == "clone" ]
		then
			source ./$VENV_NAME/bin/activate
			cd $GIT_DIR
			dependency
		else 
			update
		fi
	else
		update
	fi
fi


