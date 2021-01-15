@echo off
python --version
if errorlevel 1 goto :errorNoPython
pip install boto3 --user
pip install boto --user
goto :delete
:errorNoPython
echo;
echo Python is not installed on your system.
echo or your PATH variable is not set correctly.
echo Now opening the download URL.
start "" "https://www.python.org/downloads/windows/"
timeout 20
goto :EOF
:delete
echo Packages installed!
echo You can delete this file if you want
timeout 15 