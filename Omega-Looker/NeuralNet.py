import numpy as np

# Define the network architecture
input_size = 9
hidden_layer_1_size = 16
hidden_layer_2_size = 16
output_size = 3

# --- Initialize weights and biases ---
# These are the trainable parameters of the network.
# We initialize them randomly.

# Weights for the first hidden layer (input_size x hidden_layer_1_size)
W1 = np.random.randn(input_size, hidden_layer_1_size) * 0.01  # Small random values
b1 = np.zeros((1, hidden_layer_1_size)) # Bias initialized to zeros

# Weights for the second hidden layer (hidden_layer_1_size x hidden_layer_2_size)
W2 = np.random.randn(hidden_layer_1_size, hidden_layer_2_size) * 0.01
b2 = np.zeros((1, hidden_layer_2_size))

# Weights for the output layer (hidden_layer_2_size x output_size)
W3 = np.random.randn(hidden_layer_2_size, output_size) * 0.01
b3 = np.zeros((1, output_size))

print("--- Network Architecture ---")
print(f"Input Layer: {input_size} nodes")
print(f"Hidden Layer 1: {hidden_layer_1_size} nodes")
print(f"Hidden Layer 2: {hidden_layer_2_size} nodes")
print(f"Output Layer: {output_size} nodes\n")

print("--- Initialized Weights and Biases (Shapes) ---")
print(f"W1 shape: {W1.shape}")
print(f"b1 shape: {b1.shape}")
print(f"W2 shape: {W2.shape}")
print(f"b2 shape: {b2.shape}")
print(f"W3 shape: {W3.shape}")
print(f"b3 shape: {b3.shape}\n")


# --- Activation Functions ---
def relu(x):
    return np.maximum(0, x)

def softmax(x):
    """Numerically stable softmax function."""
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

# --- Forward Propagation (how data flows through the network) ---
def forward_propagation(X, W1, b1, W2, b2, W3, b3):
    # Input to first hidden layer
    Z1 = np.dot(X, W1) + b1  # Weighted sum + bias
    A1 = relu(Z1)  # Apply ReLU activation

    # First hidden layer to second hidden layer
    Z2 = np.dot(A1, W2) + b2
    A2 = relu(Z2)

    # Second hidden layer to output layer
    Z3 = np.dot(A2, W3) + b3
    A3 = softmax(Z3)  # Apply softmax activation for classification

    return A3

# --- Example Usage (Forward Pass) ---
# Create some dummy input data (e.g., a single sample)
# Input features would typically be normalized between 0 and 1, or -1 and 1.
input_data = np.random.rand(1, input_size)
print(f"Example Input Data (shape {input_data.shape}):\n{input_data}\n")

# Perform forward propagation
output_probabilities = forward_propagation(input_data, W1, b1, W2, b2, W3, b3)

print(f"Output Probabilities (shape {output_probabilities.shape}):\n{output_probabilities}\n")
print(f"Sum of output probabilities: {np.sum(output_probabilities):.4f}")
