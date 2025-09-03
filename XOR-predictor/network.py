import numpy as np
import math
import matplotlib.pyplot as plt

epochs = 60000 
inputLayerSize, hiddenLayerSize, outputLayerSize = 2, 3, 1
hiddenLayerCount = 3  # Number of hidden layers
LR = 0.1 # learning rate

# input data
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) # all possible inputs
y = np.array([[0], [1], [1], [0]]) # correct outputs

# Function for sigmoid activation
def sigmoid(x): 
    return 1 / (1 + np.exp(-x))

# Function for the derivative of sigmoid
def sigmoid_prime(x): 
    return x * (1 - x)

# Initialize weights for each layer
weights = []
# Weights for the first hidden layer
weights.append(np.random.uniform(size=(inputLayerSize, hiddenLayerSize)))
# Weights for the subsequent hidden layers
for _ in range(hiddenLayerCount - 1): 
    weights.append(np.random.uniform(size=(hiddenLayerSize, hiddenLayerSize)))
# Weights for the output layer
weights.append(np.random.uniform(size=(hiddenLayerSize, outputLayerSize)))

# Main training loop
for epoch in range(epochs):
    # Forward Pass
    layer_outputs = [X]
    current_input = X
    # Propagate through hidden layers
    for i in range(hiddenLayerCount):
        current_input = sigmoid(np.dot(current_input, weights[i]))
        layer_outputs.append(current_input)
    # Calculate final output
    output = np.dot(layer_outputs[-1], weights[-1])
    layer_outputs.append(output)

    # Calculate Error
    error = (y - output)

    if epoch % 5000 == 0:
        print(f'error sum {np.sum(error)}')

    # Backward Pass
    # Compute output layer delta
    dZ = error * LR
    # Update output layer weights
    weights[-1] += layer_outputs[-2].T.dot(dZ)

    # Propagate back through hidden layers
    for i in range(hiddenLayerCount - 1, -1, -1):
        dH = dZ.dot(weights[i+1].T) * sigmoid_prime(layer_outputs[i+1])
        dZ = dH
        weights[i] += layer_outputs[i].T.dot(dH)

# Test the trained network on the input data
print("\nTesting the trained network:")
for i in range(len(X)):
    current_input = X[i]
    for j in range(hiddenLayerCount):
        current_input = sigmoid(np.dot(current_input, weights[j]))
    final_output = np.dot(current_input, weights[-1])
    print(f"Input: {X[i]}, Prediction: {np.round(final_output)}")

