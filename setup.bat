@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies (this may take 10-15 minutes)...
pip install dlib-bin==19.24.6
pip install face-recognition==1.3.0
pip install Flask==2.3.3
pip install Flask-SocketIO==5.3.0
pip install opencv-python==4.6.0.66
pip install numpy>=1.26.0
pip install Pillow

echo Creating directories...
mkdir templates 2>nul
mkdir static 2>nul
mkdir images 2>nul

echo Setup complete! Run 'run.bat' to start the application.
pause