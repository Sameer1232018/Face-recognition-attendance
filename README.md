# Face Recognition Attendance System

This project implements an attendance system using face recognition technology. It leverages the `face_recognition` library, which is built on top of `dlib`, to detect and recognize faces in real-time, and stores attendance records in a MySQL database.

## Features

- **Face Detection**: Detects faces in real-time using a webcam.
- **Face Recognition**: Identifies recognized faces and marks attendance.
- **Database Integration**: Stores attendance records in a MySQL database.
- **User-Friendly Interface**: Simple and intuitive web-based UI for capturing and managing attendance.

## Requirements

Before running the project, make sure you have the following dependencies installed:

- Python 3.6+
- `face_recognition` library
- `dlib` library
- `opencv-python` library
- `numpy` library
- `mysql-connector-python` library
- Flask

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/face-recognition-attendance-system.git
    cd face-recognition-attendance-system
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install face_recognition dlib opencv-python numpy mysql-connector-python Flask
    ```

4. **Set up the MySQL database**:
    - Install MySQL server and create a database named `attendance_system`.
    - Create a table named `attendance` with the following structure:
        ```sql
        CREATE TABLE attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL
        );
        ```
    - Create a `db.py` file with the following content to handle the database connection:
        ```python
        import mysql.connector

        def connect_db():
            try:
                conn = mysql.connector.connect(
                    host='localhost',  # Replace with your host
                    user='root',       # Replace with your MySQL username
                    password='password',  # Replace with your MySQL password
                    database='attendance_system'
                )
                return conn
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return None
        ```

## Usage

1. **Add Known Faces**:
   - Place images of known individuals in the `images` directory. Ensure the images are named with the person's name (e.g., `john_doe.jpg`).

2. **Run the Application**:
    ```bash
    python app.py
    ```

3. **Access the Application**:
   - Open your web browser and go to `http://127.0.0.1:5000/`.
   - The system will automatically detect and recognize faces in the video feed.
   - Recognized faces will be marked as present in the attendance database.

## Directory Structure

