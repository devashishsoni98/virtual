from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import face_recognition
import json
import base64
import numpy as np
import cv2
import io
from PIL import Image

app = Flask(__name__)
socketio = SocketIO(app, max_http_buffer_size=16*1024*1024)  # Increased buffer size for larger images

# Load user data from JSON file
with open('users.json') as f:
    users = json.load(f)

# Create lists for known encodings and user data
known_encodings = []
known_names = []
known_ages = []
known_designations = []
known_registration_nos = []
known_mob_nos = []
known_sections = []
known_emails = []
known_years = []

# Load each user's data and prepare for recognition
for user in users:
    try:
        # Look for image file in images directory
        image_path = f"images/{user['Name'].replace(' ', '_').lower()}.jpg"
        # Try different extensions if jpg doesn't exist
        import os
        if not os.path.exists(image_path):
            image_path = f"images/{user['Name'].replace(' ', '_').lower()}.jpeg"
        if not os.path.exists(image_path):
            image_path = f"images/{user['Name'].replace(' ', '_').lower()}.png"
        
        if not os.path.exists(image_path):
            print(f"Warning: Image not found for {user['Name']} at {image_path}")
            continue
            
        known_image = face_recognition.load_image_file(image_path)
        known_encoding = face_recognition.face_encodings(known_image)[0]
        
        known_encodings.append(known_encoding)
        known_names.append(user.get('Name', 'Unknown'))
        known_ages.append(user.get('Age', 'N/A'))
        known_designations.append(user.get('Designation', 'Unknown'))
        known_registration_nos.append(user.get('Registration No.', 'N/A'))
        known_mob_nos.append(user.get('Mob. No.', 'N/A'))
        known_sections.append(user.get('Section', 'N/A'))
        known_emails.append(user.get('Email', 'N/A'))
        known_years.append(user.get('Year', 'N/A'))
    except Exception as e:
        print(f"Error loading user data for {user.get('Name', 'Unknown')}: {str(e)}")

def process_image_data(image_data):
    """
    Process the image data and return face encodings
    """
    try:
        np_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Failed to decode image")

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        height, width = image_rgb.shape[:2]
        max_size = 800
        if height > max_size or width > max_size:
            scale = max_size / max(height, width)
            new_size = (int(width * scale), int(height * scale))
            image_rgb = cv2.resize(image_rgb, new_size)

        face_locations = face_recognition.face_locations(image_rgb)
        if not face_locations:
            return None, "No face found in the image"
            
        face_encodings = face_recognition.face_encodings(image_rgb, face_locations)
        if not face_encodings:
            return None, "Could not encode face features"
            
        return face_encodings[0], None
        
    except Exception as e:
        return None, f"Error processing image: {str(e)}"

def verify_identity(face_encoding):
    """
    Compare face encoding with known encodings and return user data if match found
    """
    try:
        # Compare against known encodings to find a match
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)  # Reduced tolerance for more accuracy
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        
        if matches:
            best_match_index = np.argmin(face_distances)  # Find the closest match
            
            # Return all relevant information for the matched user
            return {
                'name': known_names[best_match_index],
                'age': known_ages[best_match_index],
                'designation': known_designations[best_match_index],
                'registration_no': known_registration_nos[best_match_index],
                'mob_no': known_mob_nos[best_match_index],
                'section': known_sections[best_match_index],
                'email': known_emails[best_match_index],
                'year': known_years[best_match_index]
            }
        else:
            return {'message': 'No match found in database'}
            
    except Exception as e:
        return {'message': f'Error during verification: {str(e)}'}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('image')
def handle_image(data):
    try:
        # Handle both camera captures and file uploads
        if isinstance(data, str) and 'data:image' in data:
            # Extract the actual base64 data
            image_data = data.split(',')[1]
            image_data = base64.b64decode(image_data)
        else:
            return emit('response', {'message': 'Invalid data received'})

        # Process the image and get face encoding
        face_encoding, error = process_image_data(image_data)
        if error:
            return emit('response', {'message': error})

        # Verify identity and return results
        result = verify_identity(face_encoding)
        emit('response', result)

    except Exception as e:
        emit('response', {'message': f'Server error: {str(e)}'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
