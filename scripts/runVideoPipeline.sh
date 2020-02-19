#!/bin/bash

export CATANA_DB_NAME=catana
export CATANA_DB_USER=catana
export CATANA_DB_PASSWORD=boghThanom
export CATANA_DB_HOST=80.211.152.51
export CATANA_DB_PORT=3306
export CATANA_DB_ENGINE=mysql

export DATA_STORAGE_PATH=/content/data

mkdir -p /content/data

cd CATANA/src/face_recognition
python3 videoPipeline.py

cd -
