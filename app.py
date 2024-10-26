from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import face_recognition
import json
import base64
import numpy as np
import cv2

app = Flask(__name__)
socketio = SocketIO(app)
# Load user data from JSON file
with open('users.json') as f:
    users = json.load(f)

# Create lists for known encodings, names, ages, roles, departments, emails, phones, and years for recognition
known_encodings = []
known_names = []
known_ages = []
known_roles = []
known_departments = []
known_emails = []
known_phones = []
known_years = []

# Load each user's data and prepare for recognition
for user in users:
    known_image = face_recognition.load_image_file(user['image_path'])
    known_encoding = face_recognition.face_encodings(known_image)[0]
    
    known_encodings.append(known_encoding)
    known_names.append(user.get('name', 'Unknown'))  # Default to 'Unknown' if name is missing
    known_ages.append(user.get('age', None))  # Default to None if age is missing
    known_roles.append(user.get('role', 'Unknown'))  # Default to 'Unknown' if role is missing
    known_departments.append(user.get('department', 'N/A'))  # Default to 'N/A' if department is missing
    known_emails.append(user.get('email', 'N/A'))  # Default to 'N/A' if email is missing
    known_phones.append(user.get('phone', 'N/A'))  # Default to 'N/A' if phone is missing
    known_years.append(user.get('year', None))  # Default to None if year is missing

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('image')
def handle_image(data):
    # Decode the base64 image data from the client
    image_data = data.split(',')[1]  # Get the base64 part
    image_data = base64.b64decode(image_data)

    # Convert binary data to numpy array for OpenCV processing
    np_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Resize the image for faster processing
    image_small = cv2.resize(image, (640, 480))

    # Find face encodings in the uploaded image
    face_encodings = face_recognition.face_encodings(image_small)
    
    if len(face_encodings) == 0:
        emit('response', {'message': 'No face found in the image'})
        return

    unknown_encoding = face_encodings[0]

    # Compare against known encodings to find a match
    matches = face_recognition.compare_faces(known_encodings, unknown_encoding)
    
    if True in matches:
        first_match_index = matches.index(True)
        
        # Retrieve all relevant information for the matched user
        name = known_names[first_match_index]
        age = known_ages[first_match_index]  
        role = known_roles[first_match_index]  
        department = known_departments[first_match_index]  
        email = known_emails[first_match_index]  
        phone = known_phones[first_match_index]  
        year = known_years[first_match_index]  

        # Send all relevant information back to the client
        emit('response', {
            'name': name,
            'age': age,
            'role': role,
            'department': department,
            'email': email,
            'phone': phone,
            'year': year
        })
        
    else:
        emit('response', {'message': 'No match found'})

if __name__ == '__main__':
    socketio.run(app, debug=True)