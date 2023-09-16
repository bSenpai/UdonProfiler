#!/usr/bin/bash

echo Uninstalling UdonProfiler ...

echo Deleting virtual environment ...
        rm -rf uprofile_venv
echo Virtual environment deleted successfully

echo Deleting logs ...
        rm uprofile.log
echo Logs deleted successfully

echo Uninstall complete!
