# ============================================================
# Diabetic Retinopathy Model Loader and Inference (INSTANT FIX)
# ============================================================

import torch
from torch import nn, optim
import torchvision
from torchvision import models, transforms
from PIL import Image
from torch.optim import lr_scheduler
import os

print("✅ Imported packages successfully")

# ============================================================
# Device Setup
# ============================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ============================================================
# Model Architecture
# ============================================================
model = models.resnet152(weights=None)  # pretrained=False equivalent
num_ftrs = model.fc.in_features
out_ftrs = 5  # 5 DR severity levels

# Replace the fully connected layer
model.fc = nn.Sequential(
    nn.Linear(num_ftrs, 512),
    nn.ReLU(),
    nn.Linear(512, out_ftrs),
    nn.LogSoftmax(dim=1)
)

criterion = nn.NLLLoss()
optimizer = optim.Adam(model.parameters(), lr=0.00001)
scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)
model.to(device)

# ============================================================
# Load Model Function — NO OPTIMIZER LOADING
# ============================================================
def load_model(path):
    """Load model weights only, skip optimizer completely."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"⚠️ Model file not found at: {path}\n"
            f"Make sure 'classifier.pt' is inside your project folder."
        )

    checkpoint = torch.load(path, map_location='cpu')

    # ✅ Load only model weights
    model.load_state_dict(checkpoint['model_state_dict'])
    print("✅ Model weights loaded successfully!")
    print("ℹ️ Optimizer loading skipped — not required for prediction.")

    return model

# ============================================================
# Inference Function
# ============================================================
def inference(model, file, transform, classes):
    """Run inference on a single retinal image."""
    file = Image.open(file).convert('RGB')
    img = transform(file).unsqueeze(0)
    print("🌀 Transforming image and sending to model...")

    model.eval()
    with torch.no_grad():
        out = model(img.to(device))
        ps = torch.exp(out)
        top_p, top_class = ps.topk(1, dim=1)
        value = top_class.item()
        predicted_class = classes[value]

        print(f"🎯 Predicted Severity Value: {value}")
        print(f"🔹 Predicted Class: {predicted_class}")

        return value, predicted_class

# ============================================================
# Model Initialization and Transforms
# ============================================================
MODEL_PATH = os.path.join(os.getcwd(), "classifier.pt")
model = load_model(MODEL_PATH)

classes = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR']

test_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.485, 0.456, 0.406),
                         std=(0.229, 0.224, 0.225))
])

# ============================================================
# Main Function
# ============================================================
def main(path):
    """Main function to get model predictions."""
    x, y = inference(model, path, test_transforms, classes)
    return x, y
    