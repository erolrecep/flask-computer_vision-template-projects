from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Define the route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for the image upload page
@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file
    file = request.files['image']

    # Save the file to the uploads folder
    file.save(os.path.join("static/uploads", file.filename))

    # Render the uploaded image on the screen
    return render_template('upload.html', filename=file.filename)

if __name__ == '__main__':
    app.run(debug=True)

