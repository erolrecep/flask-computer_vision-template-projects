from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Load the pre-trained Haar Cascade face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# OpenCV video capture object
cap = cv2.VideoCapture(0)

# Define route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Define route for video feed
@app.route('/video_feed')
def video_feed():
    def gen():
        while True:
            # Read a frame from the video stream
            success, frame = cap.read()

            # If a frame was successfully read, detect faces in the frame and draw rectangles around them
            if success:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Encode the frame as a jpeg image and yield it
                ret, jpeg = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            else:
                break

    # Use the Response class to stream video frames back to the web app
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

