<div align="center">

# 🩺 **Retinal Blindness (Diabetic Retinopathy) Detection**
### _An AI-Powered GUI System for Intelligent Retinal Screening_

---

👩‍💻 **Developed by:**  
**Nhowmitha Suresh**  
_3rd Year | B.Tech – Artificial Intelligence & Data Science_  
📧 **Email:** [nhowmi05@gmail.com](mailto:nhowmi05@gmail.com)  
🔗 **LinkedIn:** [Nhowmitha Suresh](https://www.linkedin.com)

---

</div>

## 🌌 Overview

**Retinal AI** is an intelligent deep learning system that detects **Diabetic Retinopathy (DR)** from retinal fundus images using **ResNet-based CNNs**.  
It automates early blindness detection and provides real-time predictions through an elegant, dark-themed **Tkinter GUI**.

🧠 The model classifies retinal scans into five severity levels — helping hospitals, clinics, and diagnostic centers to identify potential blindness risks *instantly and accurately.*

---

## 💡 Problem Statement

> Diabetic Retinopathy is the **leading cause of preventable blindness** among working-age adults.

- Manual retinal image grading requires expert ophthalmologists and is time-intensive.
- Early detection can prevent blindness — but screening large populations manually is **not scalable**.

Hence, the **need for AI** — a fast, reliable, and affordable DR detection system.

---

## 🚀 Motivation

In rural and under-resourced areas, ophthalmologists are scarce.  
This project aims to **bridge the healthcare gap** by providing an **AI-powered retinal screening assistant**.

🕊️ Inspired by:
- **Aravind Eye Hospital (Madurai, Tamil Nadu)**
- **Asia Pacific Tele-Ophthalmology Society (APTOS)**  

These institutions emphasize making eye care *affordable, accessible, and AI-integrated* across India.

---

## 🧠 Solution Overview

A pretrained **ResNet152** (PyTorch) model fine-tuned to classify 5 DR severity levels:

| Label | Condition |
|:------:|:-----------|
| 0 | 🟢 No DR |
| 1 | 🟡 Mild |
| 2 | 🟠 Moderate |
| 3 | 🔴 Severe |
| 4 | ⚫ Proliferative DR |

The GUI-based system allows users to:
- Log in / Sign up securely  
- Upload retinal fundus images  
- Get real-time DR predictions  
- Store and review results locally  

---

## 🧩 Key Features

✅ **AI-based DR Classification (ResNet152/ResNet18)**  
✅ **Dark-themed GUI** with gradient & neon hover effects  
✅ **SQLite Integration** for Login & Report Storage  
✅ **Offline Execution** – works without internet  
✅ **About, Contact & Review Pages** integrated  
✅ **Doctor Directory (Tamil Nadu)** with real-time contacts  
✅ **Future-ready modular design** for hospital integration  

---

## 🧰 Technologies Used

| Category | Tools / Libraries |
|:----------|:----------------|
| **Deep Learning** | PyTorch, TorchVision |
| **GUI Development** | Tkinter |
| **Image Processing** | Pillow (PIL), OpenCV |
| **Database** | SQLite |
| **Programming Language** | Python 3.11 |
| **IDE** | Visual Studio Code |
| **OS Tested** | Windows 10 / 11 |

---

## 📦 Folder Structure

Retinal_AI/
│
├── blindness.py # Tkinter GUI (Main application)
├── model.py # CNN Model Definition (ResNet)
├── classifier.pt # Trained model weights (local)
├── dr_users.db # SQLite Database
├── train_model.py # Model Training Script
├── prepare_data.py # Dataset Preparation Script
├── images/ # Screenshots for README
├── sampleimages/ # Demo retinal images
└── requirements.txt # Python dependencies

yaml
Copy code

---

## 🖥️ System Workflow

[1] User Login / Signup
↓
[2] Upload Retinal Image
↓
[3] AI Model Predicts DR Severity
↓
[4] Prediction Displayed in GUI
↓
[5] Data Saved to SQLite Database

yaml
Copy code

---

## 🖼️ GUI Snapshots

### 🔐 Login & Signup
![Login Page](images/gui1.JPG)

### 🩻 Prediction Window
![Prediction Page](images/gui3.JPG)

### 📊 DR Classification Visualization
![DR Visualization](images/mat.png)

---

## 🧪 Dataset

📂 **Dataset Used:** [APTOS 2019 Blindness Detection](https://www.kaggle.com/competitions/aptos2019-blindness-detection/data)

- 3,662 high-resolution retinal images labeled with DR severity (0–4)
- Images preprocessed (resized, normalized)
- Train/Validation split used for model training

---

## 🔬 Model Architecture

- **Base Model:** ResNet152 (PyTorch pretrained)
- **Output Layer:** 5 neurons (Softmax for 5 DR stages)
- **Loss Function:** NLLLoss  
- **Optimizer:** Adam (lr = 1e-5)
- **Validation Accuracy:** ~85.6%  
- **Training Duration:** 2–5 Epochs (depending on model type)

---

## ⚙️ How to Run Locally

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
2️⃣ Run the Application
bash
Copy code
python blindness.py
3️⃣ Default Credentials
Username	Password
admin	admin123

4️⃣ Upload Retinal Image
Select any .jpg or .png image → Get instant AI prediction.

🩺 Contact Ophthalmologists (Tamil Nadu)
Hospital	Location	Contact
Aravind Eye Hospital	Madurai	+91 452 435 6100
Sankara Nethralaya	Chennai	+91 44 4227 1500
Dr. Agarwal’s Eye Hospital	Coimbatore	+91 422 4411 111
Lotus Eye Hospital	Salem	+91 427 2770 777
Vasan Eye Care	Trichy	+91 431 241 4444

📞 Contacts are for legitimate clinical reference only.

💬 Review & Feedback Page
Patients can provide:

Service satisfaction

Clarity of diagnosis

Doctor consultation feedback

🗂️ Feedback gets stored in dr_users.db automatically.

🌟 Future Enhancements
🔹 Web deployment (Flask / Streamlit)
🔹 Federated Learning for privacy-focused AI
🔹 Explainable AI visualizations for medical transparency
🔹 Real hospital API integration
🔹 Multi-language GUI (English + Tamil)

🧑‍💻 Developer Info
👩 Nhowmitha Suresh
📚 3rd Year – B.Tech (AI & DS)
📧 nhowmi05@gmail.com
📍 Tamil Nadu, India 🇮🇳

💖 Acknowledgments
This work is inspired by the vision of:

🏥 Aravind Eye Hospital, Madurai

🌐 APTOS (Asia Pacific Tele-Ophthalmology Society)

Their mission to make eye care accessible to everyone inspired this project.

🩶 Quote
“Empowering Vision Through Intelligence.” 👁️

<div align="center">
💫 If you found this project inspiring, give it a ⭐ on GitHub!
Together, let’s advance AI in healthcare. 🧠💙

</div> ```
✅ What You Should Do Now
Copy the above into a new file named README.md

Place it in your main project folder (Retinal_AI/)

Run these commands:

bash
Copy code
git add README.md
git commit -m "Added professional dark-themed README.md"
git push origin main
Visit your repo →
👉 https://github.com/Nhowmitha-suresh/Retinal_AI
You’ll see your README come alive beautifully ✨
