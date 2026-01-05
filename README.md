<div align="center">

# 🩺 **Retinal AI – Diabetic Retinopathy Detection Network**
### _AI-Powered Retinal Blindness Detection System (Tamil Nadu Network)_

---

👩‍💻 **Developed by:**  
**Nhowmitha Suresh**  
_3rd Year | B.Tech – Artificial Intelligence & Data Science_  
📧 [nhowmi05@gmail.com](mailto:nhowmi05@gmail.com)  
🔗 [LinkedIn – Nhowmitha Suresh](https://www.linkedin.com)  

---
## 🖼️ GUI Snapshots

<img width="1218" height="807" alt="Screenshot 2025-11-08 180030" src="https://github.com/user-attachments/assets/b659facc-25af-4d94-8ebb-77e6cf4a2d1d" />
<img width="1212" height="823" alt="Screenshot 2025-11-08 180142" src="https://github.com/user-attachments/assets/1dac759d-a43a-487b-b62c-fa0428b449a6" />
<img width="1200" height="795" alt="Screenshot 2025-11-08 181022" src="https://github.com/user-attachments/assets/82500b65-4243-45e4-8d17-d935df6fb865" />


</div>

## 🌌 Overview

**Retinal AI** is a deep learning–based system designed to detect and classify **Diabetic Retinopathy (DR)** severity from retinal fundus images.  
It uses **ResNet-based CNN models (PyTorch)** and a **modern Tkinter GUI** with a dark gradient theme for a professional hospital interface.

The system allows clinicians and users to upload retinal images, get real-time DR predictions, view reports, and access verified ophthalmologists across **Tamil Nadu**.

---

## 💡 Problem Statement

> Diabetic Retinopathy (DR) is the leading cause of preventable blindness in adults.

- Manual diagnosis requires trained ophthalmologists and is time-consuming.  
- Lack of experts in rural areas delays detection and treatment.  
- AI-based screening systems can reduce diagnostic load and save vision early.

---

## 🚀 Motivation

In Tamil Nadu and similar regions, early detection of DR can prevent permanent blindness.  
**Retinal AI** supports medical professionals by providing fast, reliable, and automated DR detection.

Inspired by institutions like:
- 🏥 **Aravind Eye Hospital (Madurai)**
- 🌐 **APTOS (Asia Pacific Tele-Ophthalmology Society)**  

These organizations aim to democratize eye care through innovation.

---

## 🧠 Solution Overview

A **ResNet-based CNN** model (trained on APTOS 2019 dataset) predicts DR severity from 0–4:

| Label | Condition |
|:------:|:-----------|
| 0 | 🟢 No DR |
| 1 | 🟡 Mild |
| 2 | 🟠 Moderate |
| 3 | 🔴 Severe |
| 4 | ⚫ Proliferative DR |

Users can log in, upload retinal images, get a diagnostic prediction, and contact nearby ophthalmologists for follow-up.

---

## 🧩 Key Features

✅ AI-based DR classification (ResNet152 / ResNet18)  
✅ Modern dark-themed GUI (Tkinter)  
✅ Gradient styling & button hover effects  
✅ SQLite-based login and user data storage  
✅ Real-time DR prediction with recommendations  
✅ Review, Contact, and About pages integrated  
✅ Offline operation (no cloud dependency)

---

## 🧰 Technologies Used

| Category | Tools / Libraries |
|:----------|:----------------|
| **Deep Learning** | PyTorch, TorchVision |
| **GUI Development** | Tkinter |
| **Image Processing** | OpenCV, Pillow (PIL) |
| **Database** | SQLite |
| **Language** | Python 3.11 |
| **IDE** | Visual Studio Code |
| **OS Tested** | Windows 10 / 11 |

---

---

---

### 🧭 Navigation Features  
- 🔐 **Login / Sign Up:** Secure user access  
- 📁 **Upload Report:** Upload and analyze retinal fundus images  
- 🩺 **Doctors Directory:** Tamil Nadu verified ophthalmologist contacts  
- 💬 **Review Page:** Collect patient feedback  
- ℹ️ **About Page:** Learn about the project  
- 🚪 **Logout:** Safely exit session  

---

## 💎 Design Aesthetic

🎨 **Theme:** Deep midnight gradient (Black → Teal → Cyan)  
💡 **Font:** Segoe UI (bold, modern)  
✨ **Buttons:** Neon hover animation  
🧠 **Framework:** Native Tkinter – optimized for hospital use  
🌙 **Mode:** Dark only (eye-friendly)

---

## 🧪 Dataset

📂 **Dataset:** [APTOS 2019 Blindness Detection](https://www.kaggle.com/competitions/aptos2019-blindness-detection/data)

- 3,662 labeled fundus images  
- Each labeled with DR severity level (0–4)  
- Preprocessed (resize, normalize, augmentation)

---

## 🔬 Model Architecture

| Component | Description |
|:-----------|:-------------|
| **Base Model** | ResNet152 (PyTorch pretrained) |
| **Output Layer** | 5 neurons (Softmax for 5 DR classes) |
| **Loss Function** | Negative Log-Likelihood Loss (NLLLoss) |
| **Optimizer** | Adam (lr = 1e-5) |
| **Validation Accuracy** | ≈ 85.6% |
| **Training Duration** | 2–5 Epochs (CPU optimized) |

---

## ⚙️ How to Run Locally

### 1️⃣ Install Dependencies
bash
pip install -r requirements.txt
2️⃣ Run the App
bash
Copy code
python blindness.py
3️⃣ Default Login
Username	Password
admin	admin123

4️⃣ Upload Retinal Image
Select any .jpg / .png → Instantly get DR severity prediction.

🩺 Verified Ophthalmologists (Tamil Nadu)
Hospital	Location	Contact
Aravind Eye Hospital	Madurai	+91 452 435 6100
Sankara Nethralaya	Chennai	+91 44 4227 1500
Dr. Agarwal’s Eye Hospital	Coimbatore	+91 422 4411 111
Lotus Eye Hospital	Salem	+91 427 2770 777
Vasan Eye Care	Trichy	+91 431 241 4444

🩶 Contacts are provided for legitimate clinical awareness only.

💬 Review & Feedback Page
Patients can:

Rate prediction accuracy

Leave feedback on interface experience

Comment on doctor recommendations

All reviews are stored securely in the local database.

🌟 Future Enhancements
🔹 Web version using Flask or Streamlit
🔹 Explainable AI (XAI) heatmaps for lesion visualization
🔹 Multi-language GUI (English & Tamil)
🔹 Federated learning for privacy-focused medical AI
🔹 Integration with hospital management systems (HMS)

🧑‍💻 Developer Info
👩 Nhowmitha Suresh
📚 3rd Year – B.Tech (AI & DS)
📧 nhowmi05@gmail.com
📍 Tamil Nadu, India 🇮🇳

💖 Acknowledgments
Special thanks to:

Aravind Eye Hospital, Madurai – for inspiring this research vision

APTOS (Asia Pacific Tele-Ophthalmology Society) – for open datasets and global awareness

🩶 Quote
“Empowering Vision Through Intelligence.” 👁️

<div align="center">
💫 If you found this project inspiring, give it a ⭐ on GitHub!
Together, let’s advance AI in healthcare. 🧠💙

</div> 
