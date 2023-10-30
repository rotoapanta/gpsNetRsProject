#!/bin/bash

# Define variables
ENV_NAME="gps_netrs_env"
ENV_PATH="/home/rotoapanta/env/"
CONDA_PREFIX="/home/rotoapanta/anaconda3/"
SCRIPT_PATH="/home/rotoapanta/Documentos/Proyects/gpsNetRsProject"
PYTHON_SCRIPT="main.py"
CONFIG_FILE="config.ini"

# Mensaje de bienvenida
echo "Welcome ${USER}."

# Redirigir la salida estándar y de error al registro
exec 1> >(logger -s -t $(basename $0)) 2>&1

# Configurar el entorno Conda
eval "$(${CONDA_PREFIX}/bin/conda shell.bash hook)"

if [ $? != 0 ]; then
    echo "Error al ejecutar gpsNetRsProject: error en la carga de Conda: CRONTAB_SCRIPT_ERROR" >&2
    exit 1
fi

# Activar el entorno Conda
conda activate ${ENV_NAME}

if [ $? != 0 ]; then
    echo "Error al ejecutar gpsNetRsProject: error al activar el entorno: CRONTAB_SCRIPT_ERROR" >&2
    exit 1
fi

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

# Navegar hacia el directorio del script Python
cd ${SCRIPT_PATH}

# Ejecutar el script Python con el archivo de configuración y redirigir la salida estándar a la salida de error
python ./${PYTHON_SCRIPT}

if [ $? != 0 ]; then
    echo "Error al ejecutar gpsNetRsProject: error al ejecutar main.py: CRONTAB_SCRIPT_ERROR" >&2
    exit 1
fi
