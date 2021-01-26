@echo off
echo Checking for prereqs...

python --version
if errorlevel 1 goto :errorNoPython
echo Python is installed...

python -c "import boto3"
if errorlevel 1 goto :errorNoBoto3
echo Boto3 is installed...

aws --version
if errorlevel 1 goto :errorNoAWScli
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
if errorlevel 1 goto :errorpip

:errorNoAWScli
pip3 install awscli --upgrade --user
if errorlevel 1 goto :errorpip

:errorpip
echo there is an issue with pip
timeout 20
goto :EOF

:start
echo prereqs installed! Starting
py src/aws_integration.py
timeout 100