import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

#######

#initialized MLflow
import mlflow
mlflow.set_tracking_uri(uri="http://localhost:5000")
mlflow.set_experiment("Wind Chill Example")

#######
# Generate data
n_samples = 500

tt = np.random.uniform(-20, 10, n_samples)  # Temperature in Celsius
ff = np.random.uniform(0, 50, n_samples)  # Wind speed in km/h

# Wind Chill Formula
wc = 13.12 + 0.6215 * tt - 11.37 * (ff ** 0.16) + 0.3965 * tt * (ff ** 0.16)

# Convert to PyTorch tensors
x_train = torch.tensor(np.column_stack((tt, ff)), dtype=torch.float32)
y_train = torch.tensor(wc, dtype=torch.float32).view(-1, 1)

##########
# Step 2: Build a Neural Network Model with Hidden Layers
class wind_chill_model(nn.Module):
    def __init__(self, hidden_dim):
        super(wind_chill_model, self).__init__()
        self.fc1 = nn.Linear(2, hidden_dim)  # First hidden layer
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)  # Second hidden layer
        self.fc3 = nn.Linear(hidden_dim, 1)  # Output layer
        self.relu = nn.ReLU()  # Activation function

    def forward(self, x):
        x = self.relu(self.fc1(x))  # Apply ReLU after the first hidden layer
        x = self.relu(self.fc2(x))  # Apply ReLU after the second hidden layer
        x = self.fc3(x)  # Output layer (no activation for regression)
        return x

hidden_dim = 20
model = wind_chill_model(hidden_dim=hidden_dim)

# Define the loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0005)


#########
# Create a validation data set
n_vsamples=100

vtt = np.random.uniform(-20, 10, n_vsamples)  # Temperature in Celsius
vff = np.random.uniform(0, 50, n_vsamples)  # Wind speed in km/h
vwc = 13.12 + 0.6215 * vtt - 11.37 * (vff ** 0.16) + 0.3965 * vtt * (vff ** 0.16)

x_val = torch.tensor(np.column_stack((vtt, vff)), dtype=torch.float32)
y_val = torch.tensor(vwc, dtype=torch.float32).view(-1, 1)


##########
# Training loop
train_loss = []  # Initialize loss list
validation_loss = [] # validation loss
n_epoch = 10000  # Set number of epochs

with mlflow.start_run(run_name="logging 01"):
  # Log the hyperparameters
  mlflow.log_params({
    "hidden_dim": hidden_dim,
  })

  for epoch in range(n_epoch):
    model.train()  # Set model to train mode
    optimizer.zero_grad()  # Clear gradients
    y_pred = model(x_train)  # Forward pass
    loss = criterion(y_pred, y_train)  # Compute loss
    loss.backward()  # Backpropagate error
    optimizer.step()  # Update weights

    train_loss.append(loss.item())  # Save loss

    y_pred=model(x_val) # predict on validateion dataset
    vloss=criterion(y_pred,y_val)
    validation_loss.append(vloss.item())

    # Print losses every 500 epochs
    if (epoch + 1) % 500 == 0:
        print(f'Epoch [{epoch + 1}/{n_epoch}], Loss: {loss.item():.4f}, val_loss: {vloss.item():.4f}')

        # Log the losses metrics
        mlflow.log_metric("loss", loss.item(), step=(epoch+1)*x_train.shape[0])
        mlflow.log_metric("val_loss", vloss.item(), step=(epoch+1)*x_train.shape[0])

###########
# Loss curve
  plt.plot(np.arange(n_epoch),train_loss,label="training loss")
  plt.plot(np.arange(n_epoch),validation_loss,label="validation loss")
  plt.yscale('log')
  plt.xlabel("epoch")
  plt.ylabel("loss")
  plt.legend()
  plt.tight_layout()
  mlflow.log_figure(plt.gcf(), "figure.png")


####
  from mlflow.models import infer_signature
  signature = infer_signature(x_val.numpy(), model(x_val).detach().numpy())
  model_info = mlflow.pytorch.log_model(model, "model", signature=signature)