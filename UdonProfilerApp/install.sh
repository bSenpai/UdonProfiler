#!/usr/bin/bash

add_repo=add-apt-repository
package_manager=apt-get
python_version=3.10

echo Installing UdonProfiler ...

echo Installing Python ...
        sudo $add_repo -y ppa:deadsnakes/ppa >/dev/null 2>&1
        sudo $package_manager update >/dev/null
        sudo $package_manager install $python_version -y >/dev/null
        sudo $package_manager install $python_version-dev >/dev/null
        sudo $package_manager install python3-pip >/dev/null
        sudo $package_manager install $python_version-venv >/dev/null
        pip3 install --upgrade pip >/dev/null
echo Python installed successfully

echo Installing Tkinter ...
        sudo $package_manager install $python_version-tk >/dev/null
echo Tkinter installed successfully

echo Creating virtual environment ...
        python3.10 -m venv uprofile_venv >/dev/null
echo Virtual environment created successfully

echo Entering virtual environtment ...
        source uprofile_venv/bin/activate >/dev/null
echo Entered virtual environment

echo Installing app dependencies ...
        pip3 install -r requirements.txt --no-warn-script-location >/dev/null
echo App dependencies installed successfully

echo Exiting virtual environment ...
        deactivate
echo Exited virtual environment

echo Creating log file ...
        touch uprofile.log
echo Log file created

echo Installation complete!
