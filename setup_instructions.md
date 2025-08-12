# Face Recognition System Setup for Windows

## Step 1: Install Required Software

### 1.1 Install Python (if not already installed)
- Download Python 3.8-3.11 from https://python.org/downloads/
- **IMPORTANT**: Check "Add Python to PATH" during installation
- Verify installation: `python --version`

### 1.2 Install Visual Studio Build Tools
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Install "C++ build tools" workload
- This is required for dlib compilation

### 1.3 Install CMake
- Download from: https://cmake.org/download/
- Add to PATH during installation
- Verify: `cmake --version`

## Step 2: Project Setup Commands

Open VS Code terminal and run these commands in order:

```bash
# Create project directory
mkdir face-recognition-system
cd face-recognition-system

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies (this may take 10-15 minutes)
pip install dlib-bin==19.24.6
pip install face-recognition==1.3.0
pip install Flask==2.3.3
pip install Flask-SocketIO==5.3.0
pip install opencv-python==4.6.0.66
pip install numpy>=1.26.0
pip install Pillow

# Create required directories
mkdir templates
mkdir static
mkdir images
```

## Step 3: Add User Images

1. Create an `images` folder in your project directory
2. Add face images for each person in `users.json`
3. Name the images exactly as specified in the JSON file's "image" field
4. Supported formats: .jpg, .jpeg, .png

## Step 4: Run the Application

```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Run the Flask application
python app.py
```

## Step 5: Access the Application

- Open your browser and go to: http://localhost:5000
- The application will start with camera mode by default
- You can switch between camera and file upload modes

## Troubleshooting

### If dlib installation fails:
```bash
pip install cmake
pip install dlib-bin
```

### If face_recognition fails:
```bash
pip install --upgrade setuptools wheel
pip install face-recognition
```

### If camera doesn't work:
- Make sure your browser has camera permissions
- Try using a different browser (Chrome recommended)
- Check if other applications are using the camera

## Important Notes

- Keep the virtual environment activated when running the app
- The first run may take longer as it processes the face encodings
- Make sure image files exist in the correct location
- The system works best with clear, front-facing photos