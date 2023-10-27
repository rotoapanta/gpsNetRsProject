#!/bin/bash
echo "Welcome ${USER}."

exec 1> >(logger -s -t $(basename $0)) 2>&1

eval "$(/$HOME/anaconda3/bin/conda shell.bash hook)"

if [ $? != 0 ]
    then
        echo "Error ejecutar gpsNetRsProject: error carga conda: CRONTAB_SCRIPT_ERROR">&2
fi

conda activate gps_netrs_env

if [ $? != 0 ]
    then
        echo "Error ejecutar gpsNetRsProject: error activar entorno CRONTAB_SCRIPT_ERROR">&2
fi
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd $DIR
python ./main.py

if [ $? != 0 ]
    then
        echo "Error ejecutar proyecto1: error ejecutar pyth.py CRONTAB_SCRIPT_ERROR">&2
fi
