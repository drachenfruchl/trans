@echo off

python --version >nul 2>&1 || (
  echo Python is not installed! (I used v3.12.3)
  pause
  exit /b
)

python -m pip install -r requirements.txt

cls 
echo Finished downloading requirements (libretranslate, pyinstaller)
echo You can close this window and delete the file
echo:

pause
exit /b