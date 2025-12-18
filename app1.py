import io
import numpy as np
from flask import Flask, request, render_template
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Dropout, Flatten, Dense

app = Flask(__name__)

# Rebuild the model architecture to match training, then load weights
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(128, 128, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Conv2D(96, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(8, activation='softmax'))
model.load_weights("model1.h5")

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/predict.html', methods=["POST"])
def predict():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'a' not in request.files or request.files['a'].filename == '':
            return render_template('predict.html', output="No file uploaded")

        label = ["cellulitis", "impetigo", "athlete_foot", "nail_fungus", "ringworm",
                 "cutaneous", "chickenpox", "shingles"]
        
        img = request.files['a']  # Get uploaded image
        test_image = image.load_img(io.BytesIO(img.read()), target_size=(128, 128))  # FIXED

        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)

        result = model.predict(test_image)
        label2 = label[np.argmax(result)]  # Get the predicted label
        output = label2

        return render_template('predict.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
