from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

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

            # If a frame was successfully read, encode it as a jpeg image and yield it
            if success:
                ret, jpeg = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            else:
                break

    # Use the Response class to stream video frames back to the web app
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
