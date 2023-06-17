import tensorflow as tf
import matplotlib.pyplot as plt

# Path to the TensorFlow Lite model (.tflite file)
model_path = 'model.tflite'

# Load the model
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Extract relevant information from input and output details
input_names = [detail['name'] for detail in input_details]
input_shapes = [detail['shape'] for detail in input_details]
output_names = [detail['name'] for detail in output_details]
output_shapes = [detail['shape'] for detail in output_details]

# Convert input shapes to strings
input_shapes_str = [str(shape) for shape in input_shapes]

# Plot input details
plt.figure(figsize=(8, 6))
plt.bar(input_names, input_shapes_str)
plt.xlabel('Input Name')
plt.ylabel('Input Shape')
plt.title('TensorFlow Lite Model Input Details')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Convert output shapes to strings
output_shapes_str = [str(shape) for shape in output_shapes]

# Plot output details
plt.figure(figsize=(8, 6))
plt.bar(output_names, output_shapes_str)
plt.xlabel('Output Name')
plt.ylabel('Output Shape')
plt.title('TensorFlow Lite Model Output Details')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
