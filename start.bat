@echo off
@REM for debugging use and 
@REM for running uncompilied python code
echo Checking for prereqs...

python --version >NUL
if errorlevel 1 goto :errorNoPython
echo Python is installed...

:packageChecks
python -c "import boto3"
if errorlevel 1 goto :errorNoBoto3
echo Boto3 is installed...

call aws --version >NUL
echo AWS cli is installed...
goto :start

:errorNoPython
echo;
echo Python is not installed on your system.
echo or your PATH variable is not set correctly.
echo Now opening the download URL.
start "" "https://www.python.org/downloads/windows/"
timeout 20
goto :EOF

:errorNoBoto3
pip install boto3 --user
goto :packageChecks

:errorNoAWScli
pip3 install awscli --upgrade
echo Create an api key
aws configure
goto :packageChecks


:start
echo prereqs installed! Starting...
python src/main.py
timeout 20