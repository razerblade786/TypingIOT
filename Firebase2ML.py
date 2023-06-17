import tensorflow as tf
import numpy as np
import pyrebase

# Initialize Firebase
config = {
        "apiKey": "AIzaSyA3bH46x_LyPJUgsPZAtlh-fDDcZ50cao4",
        "authDomain": "suhaibhumid.firebaseapp.com",
        "databaseURL": "https://suhaibhumid-default-rtdb.firebaseio.com",
        "projectId": "suhaibhumid",
        "storageBucket": "suhaibhumid.appspot.com",
        "messagingSenderId": "924618277712",
        "appId": "1:924618277712:web:ce2ae64ba99745527ca255",
        "measurementId": "G-W9LQQ41SY7"
        }

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Fetch data from Firebase
data = db.child("typing_speed_logs").get().val()
profiles = ['Suhaib', 'Salehin', 'Mustafa']
print(data)

characters = []
deltas = []
times = []
output = []
for idx, profile in enumerate(profiles):
    profile_data = data.get(profile, [])
    
    try:
        for entry in list(profile_data.values())[0]:
            print(entry)
            characters.append(entry['character'])
            deltas.append(entry['delta'])
            times.append(entry['time'])
            
            temp_out = [0,0,0]
            temp_out[idx] = 1
            
            output.append(temp_out)
    except: 
        continue #
# Prepare the data for training
"""input_temp = [] # deprecated
for idx in range(len(deltas)):
    input_temp.append(times[idx])
    input_temp.append(deltas[idx])
"""
times_np = np.array(times, dtype=np.float32)
deltas_np = np.array(deltas, dtype=np.float32)
input_data = np.column_stack((deltas_np, times_np))


#input_data = np.array(input_np, dtype=np.float32)
output_data = np.array(output, dtype = np.float32)
# Define the model architecture
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(input_data, output_data, epochs=10)

# Convert the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
