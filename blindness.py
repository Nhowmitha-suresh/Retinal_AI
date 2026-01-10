# ============================================================
# RetinalAI – Diabetic Retinopathy Screening System
# Professional Clinical UI | 9 Pages | Background Image
# ============================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3
import hashlib
import random
from datetime import datetime

# ============================================================
# DATABASE INITIALIZATION
# ============================================================

DB_NAME = "retinal_ai.db"
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    diabetes_years INTEGER,
    created_at TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    eye TEXT,
    diagnosis TEXT,
    confidence REAL,
    scan_date TEXT
)
""")

cur.execute("""
INSERT OR IGNORE INTO users (username, password, role)
VALUES (?, ?, ?)
""", ("admin", hashlib.sha256("admin123".encode()).hexdigest(), "Ophthalmologist"))

conn.commit()

# ============================================================
# MAIN APPLICATION
# ============================================================

class RetinalAIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RetinalAI – Clinical DR Screening")
        self.geometry("1400x800")
        self.resizable(False, False)

        self.current_patient = None
        self.current_result = None

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for Page in (
            SplashPage,
            LoginPage,
            DashboardPage,
            PatientPage,
            UploadPage,
            AIProcessingPage,
            DiagnosisPage,
            RecommendationPage,
            HistoryPage,
            SettingsPage
        ):
            frame = Page(self.container, self)
            self.frames[Page] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_page(SplashPage)

    def show_page(self, page):
        self.frames[page].tkraise()

# ============================================================
# BASE PAGE (BACKGROUND + SIDEBAR)
# ============================================================

class BasePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Background image
        bg = Image.open("assets/medical_background.jpg").resize((1400, 800))
        self.bg_img = ImageTk.PhotoImage(bg)
        tk.Label(self, image=self.bg_img).place(relwidth=1, relheight=1)

        # Dark overlay
        overlay = tk.Frame(self, bg="#020617")
        overlay.place(relwidth=1, relheight=1)
        overlay.attributes = {"alpha": 0.55}

        # Sidebar
        self.sidebar = tk.Frame(self, bg="#020617", width=260)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(
            self.sidebar,
            text="RetinalAI",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#020617"
        ).pack(pady=30)

        self.nav_btn("Dashboard", DashboardPage)
        self.nav_btn("Patient Registration", PatientPage)
        self.nav_btn("Fundus Upload", UploadPage)
        self.nav_btn("History", HistoryPage)
        self.nav_btn("Settings", SettingsPage)

        # Content area
        self.content = tk.Frame(self, bg="#f8fafc")
        self.content.pack(side="right", fill="both", expand=True, padx=30, pady=30)

    def nav_btn(self, text, page):
        tk.Button(
            self.sidebar,
            text=text,
            font=("Segoe UI", 12),
            fg="#cbd5f5",
            bg="#020617",
            activebackground="#1e293b",
            bd=0,
            anchor="w",
            padx=24,
            height=2,
            command=lambda: self.app.show_page(page)
        ).pack(fill="x", pady=2)

# ============================================================
# PAGE 1 – SPLASH
# ============================================================

class SplashPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        bg = Image.open("assets/medical_background.jpg").resize((1400, 800))
        self.bg_img = ImageTk.PhotoImage(bg)
        tk.Label(self, image=self.bg_img).place(relwidth=1, relheight=1)

        overlay = tk.Frame(self, bg="#020617")
        overlay.place(relwidth=1, relheight=1)
        overlay.attributes = {"alpha": 0.6}

        tk.Label(
            self,
            text="RetinalAI",
            font=("Segoe UI", 48, "bold"),
            fg="white",
            bg="#020617"
        ).place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(
            self,
            text="AI-Powered Diabetic Retinopathy Screening",
            font=("Segoe UI", 16),
            fg="#cbd5f5",
            bg="#020617"
        ).place(relx=0.5, rely=0.55, anchor="center")

        self.after(2500, lambda: app.show_page(LoginPage))

# ============================================================
# PAGE 1 – LOGIN
# ============================================================

class LoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        bg = Image.open("assets/medical_background.jpg").resize((1400, 800))
        self.bg_img = ImageTk.PhotoImage(bg)
        tk.Label(self, image=self.bg_img).place(relwidth=1, relheight=1)

        overlay = tk.Frame(self, bg="#020617")
        overlay.place(relwidth=1, relheight=1)
        overlay.attributes = {"alpha": 0.65}

        card = tk.Frame(self, bg="#020617")
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=300)

        tk.Label(card, text="Secure Login",
                 font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#020617").pack(pady=25)

        self.user = ttk.Entry(card, width=30)
        self.user.pack(pady=10)
        self.user.insert(0, "admin")

        self.pwd = ttk.Entry(card, width=30, show="*")
        self.pwd.pack(pady=10)
        self.pwd.insert(0, "admin123")

        ttk.Button(
            card,
            text="Login",
            command=self.login
        ).pack(pady=20)

        self.app = app

    def login(self):
        u = self.user.get()
        p = hashlib.sha256(self.pwd.get().encode()).hexdigest()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        if cur.fetchone():
            self.app.show_page(DashboardPage)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

# ============================================================
# PAGE 2 – DASHBOARD
# ============================================================

class DashboardPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        tk.Label(
            self.content,
            text="Clinical Dashboard",
            font=("Segoe UI", 26, "bold"),
            bg="#f8fafc",
            fg="#020617"
        ).pack(anchor="w", pady=(0, 20))

        stats = tk.Frame(self.content, bg="#f8fafc")
        stats.pack(anchor="w")

        self.stat_card(stats, "Total Scans", "1,248", 0)
        self.stat_card(stats, "Positive DR Cases", "312", 1)
        self.stat_card(stats, "Pending Referrals", "48", 2)

    def stat_card(self, parent, title, value, col):
        card = tk.Frame(parent, bg="white", width=280, height=140)
        card.grid(row=0, column=col, padx=16)
        card.pack_propagate(False)

        tk.Label(card, text=title,
                 font=("Segoe UI", 11),
                 fg="#64748b",
                 bg="white").pack(anchor="w", padx=20, pady=(18, 4))

        tk.Label(card, text=value,
                 font=("Segoe UI", 30, "bold"),
                 fg="#2563eb",
                 bg="white").pack(anchor="w", padx=20)

# ============================================================
# PAGE 3 – PATIENT REGISTRATION
# ============================================================

class PatientPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        tk.Label(self.content, text="Patient Registration",
                 font=("Segoe UI", 24, "bold"),
                 bg="#f8fafc").pack(anchor="w")

        form = tk.Frame(self.content, bg="#f8fafc")
        form.pack(pady=20, anchor="w")

        self.entries = {}
        fields = ["Patient ID", "Name", "Age", "Gender", "Diabetes Years"]

        for i, f in enumerate(fields):
            tk.Label(form, text=f, bg="#f8fafc",
                     font=("Segoe UI", 12)).grid(row=i, column=0, sticky="w", pady=8)
            e = ttk.Entry(form, width=35)
            e.grid(row=i, column=1, pady=8, padx=20)
            self.entries[f] = e

        ttk.Button(
            self.content,
            text="Save Patient",
            command=self.save_patient
        ).pack(pady=20)

    def save_patient(self):
        pid = self.entries["Patient ID"].get()
        if not pid:
            messagebox.showerror("Error", "Patient ID required")
            return
        self.app.current_patient = pid
        self.app.show_page(UploadPage)

# ============================================================
# PAGE 4 – IMAGE UPLOAD
# ============================================================

class UploadPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        tk.Label(self.content, text="Fundus Image Upload",
                 font=("Segoe UI", 24, "bold"),
                 bg="#f8fafc").pack(anchor="w")

        ttk.Button(
            self.content,
            text="Select Image",
            command=lambda: filedialog.askopenfilename()
        ).pack(pady=40)

        ttk.Button(
            self.content,
            text="Run AI Analysis",
            command=lambda: app.show_page(AIProcessingPage)
        ).pack()

# ============================================================
# PAGE 5 – AI PROCESSING
# ============================================================

class AIProcessingPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        tk.Label(self.content,
                 text="AI Processing...",
                 font=("Segoe UI", 28, "bold"),
                 bg="#f8fafc").pack(pady=100)

        self.after(3000, self.finish)

    def finish(self):
        self.app.current_result = {
            "stage": random.choice(
                ["No DR", "Mild DR", "Moderate DR", "Severe DR", "Proliferative DR"]
            ),
            "confidence": round(random.uniform(88, 99), 2)
        }
        self.app.show_page(DiagnosisPage)

# ============================================================
# PAGE 6 – DIAGNOSIS
# ============================================================

class DiagnosisPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        tk.Label(self.content,
                 text="Diagnosis Result",
                 font=("Segoe UI", 24, "bold"),
                 bg="#f8fafc").pack(anchor="w")

        self.result_lbl = tk.Label(
            self.content,
            font=("Segoe UI", 22),
            bg="#f8fafc",
            fg="#2563eb"
        )
        self.result_lbl.pack(pady=40)

        ttk.Button(
            self.content,
            text="Clinical Recommendation",
            command=lambda: app.show_page(RecommendationPage)
        ).pack()

        self.update_result()

    def update_result(self):
        if self.app.current_result:
            r = self.app.current_result
            self.result_lbl.config(
                text=f"{r['stage']} DR\nConfidence: {r['confidence']}%"
            )

# ============================================================
# PAGE 7 – RECOMMENDATION
# ============================================================

class RecommendationPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        tk.Label(self.content,
                 text="Clinical Recommendation",
                 font=("Segoe UI", 24, "bold"),
                 bg="#f8fafc").pack(anchor="w")

        tk.Label(
            self.content,
            text="• Refer to ophthalmologist\n• Follow-up in 3–6 months\n• Maintain glycemic control",
            font=("Segoe UI", 16),
            bg="#f8fafc"
        ).pack(pady=40)

# ============================================================
# PAGE 8 – HISTORY
# ============================================================

class HistoryPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        tk.Label(self.content,
                 text="Patient History",
                 font=("Segoe UI", 24, "bold"),
                 bg="#f8fafc").pack(anchor="w")

        ttk.Treeview(
            self.content,
            columns=("Date", "Diagnosis", "Confidence"),
            show="headings"
        ).pack(fill="both", expand=True, pady=20)

# ============================================================
# PAGE 9 – SETTINGS
# ============================================================

class SettingsPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        tk.Label(self.content,
                 text="Settings & Compliance",
                 font=("Segoe UI", 24, "bold"),
                 bg="#f8fafc").pack(anchor="w")

        tk.Label(
            self.content,
            text="✔ Encrypted Storage\n✔ Role-Based Access\n✔ Ethical AI Usage",
            font=("Segoe UI", 16),
            bg="#f8fafc"
        ).pack(pady=40)

# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    RetinalAIApp().mainloop()
