#!/usr/bin/bash

source uprofile_venv/bin/activate
python ./UdonProfiler.py > ./uprofile.log 2>&1
deactivate
