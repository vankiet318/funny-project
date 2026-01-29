import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

train_dataset = pd.read_csv('mnist_train.csv')

X_train = train_dataset.iloc[:, 1:].values.reshape(-1, 28, 28)
y_train = train_dataset.iloc[:, 0].values

test_dataset = pd.read_csv('mnist_test.csv')
X_test = test_dataset.iloc[:, 1:].values.reshape(-1, 28, 28)
y_test = test_dataset.iloc[:, 0].values

def display_sample_images(X, y_pred, y_true, num_images=5):
    plt.figure(figsize=(20, 2))
    for i in range(num_images):
        plt.subplot(1, num_images, i + 1)
        plt.imshow(X[i], cmap='gray')
        plt.title(f'Pred: {y_pred[i]}, True: {y_true[i]}')
        plt.axis('off')
    plt.show()

class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01):
        self.lr = learning_rate

        # Weight initialization - He initialization for ReLU (推奨される初期化方法)
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((1, hidden_size))

        self.W2 = np.random.randn(hidden_size, 64) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros((1, 64))

        self.W3 = np.random.randn(64, 32) * np.sqrt(2.0 / 64)
        self.b3 = np.zeros((1, 32))

        self.W4 = np.random.randn(32, 64) * np.sqrt(2.0 / 32)
        self.b4 = np.zeros((1, 64))

        self.W5 = np.random.randn(64, 32) * np.sqrt(2.0 / 64)
        self.b5 = np.zeros((1, 32))

        self.W6 = np.random.randn(32, output_size) * np.sqrt(2.0 / 32)
        self.b6 = np.zeros((1, output_size))

    # Activation functions
    def relu(self, z):
        return np.maximum(0, z)

    def relu_derivative(self, z):
        return (z > 0).astype(float)

    def softmax(self, z):
        exp = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp / np.sum(exp, axis=1, keepdims=True)

    # Forward pass
    def forward(self, X):
        self.Z1 = np.dot(X, self.W1) + self.b1
        self.A1 = self.relu(self.Z1)

        self.Z2 = np.dot(self.A1, self.W2) + self.b2
        self.A2 = self.relu(self.Z2)

        self.Z3 = np.dot(self.A2, self.W3) + self.b3
        self.A3 = self.relu(self.Z3)

        self.Z4 = np.dot(self.A3, self.W4) + self.b4
        self.A4 = self.relu(self.Z4)

        self.Z5 = np.dot(self.A4, self.W5) + self.b5
        self.A5 = self.relu(self.Z5)

        self.Z6 = np.dot(self.A5, self.W6) + self.b6
        self.A6 = self.softmax(self.Z6)

        return self.A6

    # Loss
    def compute_loss(self, y_true, y_pred):
        loss = -np.mean(np.sum(y_true * np.log(y_pred + 1e-8), axis=1))
        return loss

    # Backpropagation
    def backward(self, X, y_true, y_pred):
        m = X.shape[0]

        # Output layer gradient
        dZ6 = y_pred - y_true
        dW6 = np.dot(self.A5.T, dZ6) / m
        db6 = np.sum(dZ6, axis=0, keepdims=True) / m

        # Hidden layer gradient
        dA5 = np.dot(dZ6, self.W6.T)
        dZ5 = dA5 * self.relu_derivative(self.Z5)
        dW5 = np.dot(self.A4.T, dZ5) / m
        db5 = np.sum(dZ5, axis=0, keepdims=True) / m

        dA4 = np.dot(dZ5, self.W5.T)
        dZ4 = dA4 * self.relu_derivative(self.Z4)
        dW4 = np.dot(self.A3.T, dZ4) / m
        db4 = np.sum(dZ4, axis=0, keepdims=True) / m

        dA3 = np.dot(dZ4, self.W4.T)
        dZ3 = dA3 * self.relu_derivative(self.Z3)
        dW3 = np.dot(self.A2.T, dZ3) / m
        db3 = np.sum(dZ3, axis=0, keepdims=True) / m

        dA2 = np.dot(dZ3, self.W3.T)
        dZ2 = dA2 * self.relu_derivative(self.Z2)
        dW2 = np.dot(self.A1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m

        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.relu_derivative(self.Z1)
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        # Update
        self.W6 -= self.lr * dW6
        self.b6 -= self.lr * db6
        self.W5 -= self.lr * dW5
        self.b5 -= self.lr * db5
        self.W4 -= self.lr * dW4
        self.b4 -= self.lr * db4
        self.W3 -= self.lr * dW3
        self.b3 -= self.lr * db3
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1

    # Training loop
    def train(self, X, y, epochs=1000):
        for epoch in range(epochs):
            y_pred = self.forward(X)
            loss = self.compute_loss(y, y_pred)
            self.backward(X, y, y_pred)
            print(f"Epoch {epoch}, Loss: {loss:.4f}")

    def predict(self, X):
        probs = self.forward(X)
        return np.argmax(probs, axis=1)

def one_hot_encode(y, num_classes):
    m = y.shape[0]
    one_hot = np.zeros((m, num_classes))
    one_hot[np.arange(m), y] = 1
    return one_hot



neural_network = SimpleNeuralNetwork(input_size=784, hidden_size=128, output_size=10, learning_rate=0.1)
X_train_flat = X_train.reshape(X_train.shape[0], -1) / 255.0
y_train_one_hot = one_hot_encode(y_train, 10)
neural_network.train(X_train_flat, y_train_one_hot, epochs=100)
X_test_flat = X_test.reshape(X_test.shape[0], -1) / 255.0
y_pred = neural_network.predict(X_test_flat)
accuracy = np.mean(y_pred == y_test) * 100
print(f'Test Accuracy: {accuracy:.2f}%')


display_sample_images(X_test, y_pred, y_test, 8)