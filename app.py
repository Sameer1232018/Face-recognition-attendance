from flask import Flask, render_template, Response
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta
from db import connect_db  # Import the database connection function

app = Flask(__name__)

# Define a cooldown period (e.g., 10 seconds)
COOLDOWN_PERIOD = timedelta(minutes=10)

# Dictionary to store recognized faces and their last attendance entry timestamps
recognized_faces = {}

# Path to the images
path = 'images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    try:
        # Get current time
        now = datetime.now()

        # Check if the recognized face exists in the dictionary
        if name in recognized_faces:
            last_mark_time = recognized_faces[name]
            # Check if enough time has passed since the last attendance entry
            if now - last_mark_time < COOLDOWN_PERIOD:
                print(f"Not enough time has passed since {name}'s last attendance entry. Skipping...")


        # Connect to the database
        conn = connect_db()
        if conn is None:
            print("Failed to connect to the database")
            return False

        cursor = conn.cursor()

        # Get current date and time
        dateString = now.strftime('%Y-%m-%d')
        dtString = now.strftime('%H:%M:%S')

        # Check if the name and date combination already exists in the database
        cursor.execute("SELECT * FROM attendance WHERE name=%s AND date=%s", (name, dateString))
        result = cursor.fetchone()

        if result is None:
            # Insert the new record into the database
            cursor.execute("INSERT INTO attendance (name, date, time) VALUES (%s, %s, %s)", (name, dateString, dtString))
            conn.commit()
            print(f"Added {name} on {dateString} at {dtString} to the database")
            recognized_faces[name] = now
            return True
        else:
            print(f"{name} already present in the database for today")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        if conn:
            conn.close()


encodeListKnown = findEncodings(images)
print('Encoding Complete')

def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        if not success:
            break
        else:
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    if markAttendance(name):
                        # You can set a flag or do something else to indicate success
                        pass

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(debug=True)
