import torch
from torch import nn

torch.manual_seed(1)

X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y = torch.tensor([[0.], [1.], [1.], [0.]])

model = nn.Sequential(nn.Linear(2, 2), nn.Sigmoid(), nn.Linear(2, 1))
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.1)

initial_loss = loss_fn(model(X), y).item()

for _ in range(5000):
    optimizer.zero_grad()
    loss = loss_fn(model(X), y)
    loss.backward()
    optimizer.step()

optimizer.zero_grad()
logits = model(X)
final_loss = loss_fn(logits, y)
final_loss.backward()
probabilities = torch.sigmoid(logits).detach().flatten()
labels = (probabilities >= 0.5).int()
gradient = model[0].weight.grad.detach().clone()

print(f"Initial loss: {initial_loss:.8f}")
print(f"Final loss: {final_loss.item():.8f}")
print("Probabilities:", probabilities.tolist())
print("Thresholded labels:", labels.tolist())
print("First-layer weight gradient:\n", gradient)
print("Loss test: PASS" if final_loss.item() < initial_loss else "Loss test: FAIL",
      "- the final loss should be lower than the initial loss.")
print("Classification test: PASS" if torch.equal(labels, y.flatten().int()) else "Classification test: FAIL",
      "- all four thresholded predictions should match the XOR targets.")
print("Gradient test: PASS" if torch.count_nonzero(gradient).item() > 0 else "Gradient test: FAIL",
      "- a nonzero parameter gradient shows that backpropagation produced an update signal.")
