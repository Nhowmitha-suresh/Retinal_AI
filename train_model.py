import os
import random
import torch
from torch import nn, optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm
from datetime import datetime

# ===============================================================
# 🔧 CONFIG
# ===============================================================
DATA_DIR = "dataset/train"
NUM_CLASSES = 5
NUM_EPOCHS = 2          # keep small for CPU testing
BATCH_SIZE = 16
LR = 1e-4
SEED = 42
PATIENCE = 3            # early stopping patience
MODEL_PATH = "classifier.pt"

# ===============================================================
# 🎯 REPRODUCIBILITY
# ===============================================================
torch.manual_seed(SEED)
random.seed(SEED)
torch.cuda.manual_seed_all(SEED)

# ===============================================================
# 🖥️ DEVICE
# ===============================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🖥️ Using device: {device}")

# ===============================================================
# 🧪 DATA TRANSFORMS
# ===============================================================
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ===============================================================
# 📦 DATASET
# ===============================================================
full_dataset = datasets.ImageFolder(DATA_DIR, transform=train_transform)

train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size

train_dataset, val_dataset = random_split(
    full_dataset, [train_size, val_size]
)

# Override transform for validation
val_dataset.dataset.transform = val_transform

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=2,
    pin_memory=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=2,
    pin_memory=True
)

print(f"📊 Total: {len(full_dataset)} | Train: {train_size} | Val: {val_size}")

# ===============================================================
# 🧠 MODEL
# ===============================================================
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
in_features = model.fc.in_features

model.fc = nn.Sequential(
    nn.Linear(in_features, 512),
    nn.ReLU(inplace=True),
    nn.Dropout(0.3),
    nn.Linear(512, NUM_CLASSES)
)

model.to(device)

# ===============================================================
# ⚙️ LOSS & OPTIMIZER
# ===============================================================
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

scaler = torch.cuda.amp.GradScaler(enabled=(device.type == "cuda"))

# ===============================================================
# 🚀 TRAINING LOOP
# ===============================================================
best_val_acc = 0.0
epochs_no_improve = 0

print("\n🚀 Training started...\n")

for epoch in range(NUM_EPOCHS):
    model.train()
    train_loss = 0.0
    correct = 0
    total = 0

    loop = tqdm(train_loader, desc=f"Epoch {epoch+1}/{NUM_EPOCHS}")
    for inputs, labels in loop:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()

        with torch.cuda.amp.autocast(enabled=(device.type == "cuda")):
            outputs = model(inputs)
            loss = criterion(outputs, labels)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        train_loss += loss.item()
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

        loop.set_postfix(loss=loss.item())

    train_acc = 100 * correct / total
    avg_train_loss = train_loss / len(train_loader)

    # ===============================================================
    # ✅ VALIDATION
    # ===============================================================
    model.eval()
    val_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            val_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    val_acc = 100 * correct / total
    avg_val_loss = val_loss / len(val_loader)

    print(
        f"\n📘 Epoch {epoch+1}"
        f" | Train Loss: {avg_train_loss:.4f}"
        f" | Train Acc: {train_acc:.2f}%"
        f" | Val Loss: {avg_val_loss:.4f}"
        f" | Val Acc: {val_acc:.2f}%"
    )

    # ===============================================================
    # 💾 SAVE BEST MODEL
    # ===============================================================
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        epochs_no_improve = 0

        torch.save({
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "num_classes": NUM_CLASSES,
            "architecture": "resnet18",
            "val_accuracy": best_val_acc,
            "timestamp": datetime.utcnow().isoformat()
        }, MODEL_PATH)

        print(f"💾 Best model saved! (Val Acc: {best_val_acc:.2f}%)")
    else:
        epochs_no_improve += 1
        if epochs_no_improve >= PATIENCE:
            print("⏹️ Early stopping triggered")
            break

print("\n🎯 Training complete")
print(f"🏆 Best Validation Accuracy: {best_val_acc:.2f}%")
print(f"📦 Model saved as: {MODEL_PATH}")
