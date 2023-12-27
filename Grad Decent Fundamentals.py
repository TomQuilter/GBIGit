import torch
import math
import numpy as np
#%%
import matplotlib.pyplot as plt    

print("hi")
# Data Generation
np.random.seed(42)
x = np.random.rand(100, 1)
y = 1 + 2 * x + .1 * np.random.randn(100, 1)

# Random intercept and gradient
a = np.random.rand()  # Random value between 0 and 1 for the gradient
b = np.random.rand() * 10  # Random value between 0 and 10 for the intercept

# Calculate y values for the straight line
y_line = [a * xi + b for xi in x]
#%%
# Create the scatter plot
plt.scatter(x, y, color='blue', marker='o')

# Plot the straight line
plt.plot(x, y_line, color='red', label=f'y = {a:.2f}x + {b:.2f}')

# Add title, labels, and legend
plt.title('Sample Scatter Plot with Straight Line')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()

# Display the plot
plt.show()







# Shuffles the indices
idx = np.arange(100)
np.random.shuffle(idx)

# Uses first 80 random indices for train
train_idx = idx[:80]
# Uses the remaining indices for validation
val_idx = idx[80:]

# Generates train and validation sets
x_train, y_train = x[train_idx], y[train_idx]
x_val, y_val = x[val_idx], y[val_idx]



# Initializes parameters "a" and "b" randomly
np.random.seed(42)
a = np.random.randn(1)
b = np.random.randn(1)

print(a, b)

# Sets learning rate
lr = 1e-1
# Defines number of epochs
n_epochs = 50

for epoch in range(n_epochs):
    
    print("###### Epoch = ", epoch, " ######")
    # Computes our model's predicted output
    yhat = a + b * x_train
    
    # How wrong is our model? That's the error! 
    error = (y_train - yhat)
    
   
    
    # It is a regression, so it computes mean squared error (MSE)
    loss = (error ** 2).mean()
    
    print("loss =", round(loss, 2))
    
    # Computes gradients for both "a" and "b" parameters
    a_grad = -2 * error.mean()
    b_grad = -2 * (x_train * error).mean()
    
    # Updates parameters using gradients and the learning rate
    a = a - lr * a_grad
    b = b - lr * b_grad
    
    print("a gradient =", round(a_grad, 2))
    
    print("b gradient = ", round(b_grad, 2))
    
        # Calculate y values for the straight line
    y_line = [a + b * xi for xi in x]
    
    # Create the scatter plot
    plt.scatter(x, y, color='blue', marker='o')
    
    # Plot the straight line
    plt.plot(x, y_line, color='red')
    
    around = np.round(a, 2)
    bround = np.round(b, 2)
    
    # Add title, labels, and legend
    plt.title(f'y= {around}x + {bround}')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis') 
    plt.legend()
    
    # Display the plot
    plt.show()
    

print("Result of Grad Descent")
    
print(a, b)

print("Result of standard regression")

# Sanity Check: do we get the same results as our gradient descent?
from sklearn.linear_model import LinearRegression
linr = LinearRegression()
linr.fit(x_train, y_train)
print(linr.intercept_, linr.coef_[0])