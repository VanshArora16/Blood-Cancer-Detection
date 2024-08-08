from flask import Flask, request, jsonify, render_template
import pickle
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

app = Flask(__name__, template_folder='templates')

# Load the trained model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
# Define the class mapping
class_mapping = {
    0: '[Benign]',
    1: '[Malignant] early Pre-B',
    2: '[Malignant] Pre-B',
    3: '[Malignant] Pro-B'
}

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define ImageDataGenerator for preprocessing images
test_datagen = ImageDataGenerator(rescale=1./255)

def process_image(image_path):
    """Process the uploaded image for prediction."""
    img = Image.open(image_path)
    img = img.resize((64, 64))
    img_array = np.array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Process the image
    processed_image = process_image(filepath)

    # Make a prediction
    prediction = model.predict(processed_image)

    # Assuming your model returns categorical prediction
    predicted_class = np.argmax(prediction)
    result = class_mapping[predicted_class]

    # Return the prediction result as JSON
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)
