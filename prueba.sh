#!/bin/bash

# Define variables
ENV_NAME="gps_netrs_env"
ENV_PATH="/home/rotoapanta/env/"
CONDA_PREFIX="/home/rotoapanta/anaconda3/"
SCRIPT_PATH="/home/rotoapanta/Documentos/Proyects/gpsNetRsProject"
PYTHON_SCRIPT="main.py"
CONFIG_FILE="config.ini"

# Validar la existencia de rutas y archivos
if [ ! -d "${SCRIPT_PATH}" ]; then
    echo "El directorio del script no existe: ${SCRIPT_PATH}"
    exit 1
fi

if [ ! -f "${SCRIPT_PATH}/${PYTHON_SCRIPT}" ]; then
    echo "El script Python no existe: ${SCRIPT_PATH}/${PYTHON_SCRIPT}"
    exit 1
fi

if [ ! -f "${SCRIPT_PATH}/${CONFIG_FILE}" ]; then
    echo "El archivo de configuración no existe: ${SCRIPT_PATH}/${CONFIG_FILE}"
    exit 1
fi

# Crear el entorno Conda si no existe
if [ ! -d "${CONDA_PREFIX}/envs/${ENV_NAME}" ]; then
    conda create --name ${ENV_NAME} python=3.10
fi

# Activar el entorno Conda
echo ${ENV_NAME}
conda activate ${ENV_NAME}

# Instalar las dependencias del archivo requirements.txt
pip install -r ${SCRIPT_PATH}/requirements.txt

# Navegar hacia el directorio del script Python
cd ${SCRIPT_PATH}

# Ejecutar el script Python con el archivo de configuración y redirigir la salida estándar a la salida de error
python ./${PYTHON_SCRIPT} >&2