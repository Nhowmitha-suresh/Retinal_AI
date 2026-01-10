import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog, messagebox
from PIL import Image
import sqlite3
import datetime
import os
import random
import matplotlib.pyplot as plt
import hashlib
import re

# =========================================================
# SAFETY & THEME
# =========================================================
ctk.deactivate_automatic_dpi_awareness()
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# =========================================================
# DUAL COLOUR SYSTEM (ONLY TWO COLOURS)
# =========================================================
SAFE_COLOR = "#007BFF"     # Medical Blue
DANGER_COLOR = "#FF4D4D"   # Red (Moderate / Severe)
CARD_BG = "#FFFFFF"
TEXT_CLR = "#1A2B3C"
TOPBAR_BG = "#E9F2FF"
SIDEBAR_BG = "#F4F8FF"

# =========================================================
# DATABASE
# =========================================================
conn = sqlite3.connect("retinal_ai.db")
cur = conn.cursor()

# users table: add role and password_hash for strong auth while supporting legacy rows
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT,
        password_hash TEXT
    )
    """
)
# ensure columns exist if DB was created earlier
def _ensure_column(table, column, coltype):
    cur.execute(f"PRAGMA table_info({table})")
    cols = [c[1] for c in cur.fetchall()]
    if column not in cols:
        try:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")
        except Exception:
            pass

_ensure_column("users", "role", "TEXT")
_ensure_column("users", "password_hash", "TEXT")

cur.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    phone TEXT,
    address TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    severity TEXT,
    confidence INTEGER,
    recommendation TEXT,
    referred TEXT,
    created_at TEXT
)
""")
conn.commit()

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def severity_color(severity):
    if severity in ["No DR", "Mild"]:
        return SAFE_COLOR
    return DANGER_COLOR

def recommendation_text(severity):
    if severity in ["No DR", "Mild"]:
        return "Regular monitoring recommended"
    return "Immediate ophthalmologist consultation required"

# password utilities
def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def is_strong_password(pw: str) -> bool:
    if len(pw) < 8:
        return False
    if not re.search(r"[A-Z]", pw):
        return False
    if not re.search(r"[a-z]", pw):
        return False
    if not re.search(r"\d", pw):
        return False
    if not re.search(r"[^A-Za-z0-9]", pw):
        return False
    return True

# =========================================================
# MAIN APP
# =========================================================
class RetinalAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RETINAL AI – Diabetic Retinopathy Detection")
        self.state("zoomed")
        self.minsize(1200, 720)

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        # ---------------- BACKGROUND IMAGE ----------------
        bg_path = "assets/bg_eye.jpg"
        if os.path.exists(bg_path):
            img = Image.open(bg_path).resize((screen_w, screen_h))
        else:
            img = Image.new("RGB", (screen_w, screen_h), "#000000")

        self.bg_img = CTkImage(light_image=img, dark_image=img, size=(screen_w, screen_h))
        ctk.CTkLabel(self, image=self.bg_img, text="").place(x=0, y=0)

        # ---------------- TOP BAR ----------------
        self.topbar = ctk.CTkFrame(self, height=60, fg_color=TOPBAR_BG)
        self.topbar.pack(fill="x")

        ctk.CTkLabel(
            self.topbar,
            text="RETINAL AI – Primary Health Centre Screening System",
            font=("Segoe UI", 20, "bold"),
            text_color=SAFE_COLOR
        ).pack(side="left", padx=20)

        # ---------------- SIDEBAR ----------------
        self.sidebar = ctk.CTkFrame(self, width=240, fg_color=SIDEBAR_BG)
        self.sidebar.place(x=0, y=60, relheight=1)

        # ---------------- MAIN CONTAINER ----------------
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(x=240, y=60, relwidth=1, relheight=1)

        # ---------------- PAGES ----------------
        self.frames = {}
        for Page in (
            LoginPage,
            RegistrationPage,
            AboutPage,
            PatientPage,
            ScanPage,
            ReportPage,
            ReportDetailPage,
            AnalyticsPage,
        ):
            frame = Page(self.container, self)
            self.frames[Page] = frame
            frame.place(relwidth=1, relheight=1)

        self.show(LoginPage)

        # ---------------- SIDEBAR BUTTONS ----------------
        buttons = [
            ("About App", AboutPage),
            ("Patient Details", PatientPage),
            ("Retinal Scan", ScanPage),
            ("AI Report", ReportPage),
            ("Medical Report", ReportDetailPage),
            ("Analytics", AnalyticsPage),
        ]

        for txt, page in buttons:
            ctk.CTkButton(
                self.sidebar,
                text=txt,
                fg_color="transparent",
                hover_color="#033e5c",
                anchor="w",
                command=lambda p=page: self.show(p)
            ).pack(fill="x", padx=12, pady=8)

    def show(self, page):
        self.frames[page].tkraise()

# =========================================================
# LOGIN PAGE
# =========================================================
class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")

        card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=16,
                            width=460, height=360)
        card.place(relx=0.5, rely=0.45, anchor="center")

        ctk.CTkLabel(card, text="Welcome to Retinal AI",
                     font=("Segoe UI", 22, "bold"),
                     text_color=SAFE_COLOR).pack(pady=18)

        self.role = ctk.CTkOptionMenu(card, values=["Doctor", "Patient"])
        self.role.set("Doctor")
        self.role.pack(pady=6)

        self.user = ctk.CTkEntry(card, placeholder_text="Username", width=320)
        self.pwd = ctk.CTkEntry(card, placeholder_text="Password", show="*", width=320)
        self.user.pack(pady=6)
        self.pwd.pack(pady=6)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(pady=14)
        ctk.CTkButton(
            btn_row, text="Login",
            fg_color=SAFE_COLOR, text_color="white",
            width=140, command=self.login
        ).pack(side="left", padx=6)
        ctk.CTkButton(
            btn_row, text="Register",
            fg_color="#6C757D", text_color="white",
            width=140, command=lambda: self.master.master.show(RegistrationPage)
        ).pack(side="left", padx=6)

    def login(self):
        u, p = self.user.get(), self.pwd.get()
        role = self.role.get()
        if not u or not p:
            messagebox.showerror("Error", "Enter credentials")
            return
        # First try hashed
        cur.execute("SELECT username FROM users WHERE username=? AND role=? AND password_hash=?",
                    (u, role, hash_password(p)))
        row = cur.fetchone()
        if not row:
            # fallback to legacy plaintext (no role filter to support older rows)
            cur.execute("SELECT username FROM users WHERE username=? AND password=?",
                        (u, p))
            row = cur.fetchone()
        if not row:
            messagebox.showerror("Login Failed", "Invalid credentials")
            return
        self.master.master.show(AboutPage)

class RegistrationPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")

        card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=16,
                            width=520, height=420)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Create Account",
                     font=("Segoe UI", 22, "bold"),
                     text_color=SAFE_COLOR).pack(pady=12)

        self.role = ctk.CTkOptionMenu(card, values=["Doctor", "Patient"])
        self.role.set("Doctor")
        self.role.pack(pady=6)

        self.user = ctk.CTkEntry(card, placeholder_text="Username", width=360)
        self.pwd = ctk.CTkEntry(card, placeholder_text="Password", show="*", width=360)
        self.pwd2 = ctk.CTkEntry(card, placeholder_text="Confirm Password", show="*", width=360)
        self.user.pack(pady=6)
        self.pwd.pack(pady=6)
        self.pwd2.pack(pady=6)

        ctk.CTkButton(
            card, text="Register",
            fg_color=SAFE_COLOR, text_color="white",
            width=200, command=self.register
        ).pack(pady=14)

        ctk.CTkButton(
            card, text="Back to Login",
            fg_color="#6C757D", text_color="white",
            width=200, command=lambda: self.master.master.show(LoginPage)
        ).pack()

    def register(self):
        u, p1, p2, role = self.user.get().strip(), self.pwd.get(), self.pwd2.get(), self.role.get()
        if not u or not p1 or not p2:
            messagebox.showerror("Error", "Fill all fields")
            return
        if p1 != p2:
            messagebox.showerror("Error", "Passwords do not match")
            return
        if not is_strong_password(p1):
            messagebox.showerror(
                "Weak Password",
                "Use at least 8 characters with upper, lower, number, and special symbol."
            )
            return
        try:
            cur.execute(
                "INSERT INTO users(username, password, role, password_hash) VALUES (?,?,?,?)",
                (u, None, role, hash_password(p1))
            )
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
            return
        messagebox.showinfo("Success", "Registration complete. Please login.")
        self.master.master.show(LoginPage)

# =========================================================
# ABOUT PAGE
# =========================================================
class AboutPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")

        card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=25,
                            width=900, height=420)
        card.place(relx=0.55, rely=0.45, anchor="center")

        ctk.CTkLabel(card, text="About Retinal AI",
                     font=("Segoe UI", 26, "bold"),
                     text_color=SAFE_COLOR).pack(pady=20)

        ctk.CTkLabel(
            card,
            text=(
                "Retinal AI is an AI-assisted Diabetic Retinopathy screening system\n"
                "designed for use in Primary Health Centres (PHCs).\n\n"
                "KEY FEATURES:\n"
                "• AI-based severity prediction\n"
                "• Dual-colour clinical UI (Safe / Danger)\n"
                "• Secure patient data storage\n"
                "• Clinical reports with confidence score\n"
                "• Referral support for ophthalmologists\n\n"
                "The system helps in early detection of diabetic eye disease,\n"
                "reducing preventable blindness through timely referral."
            ),
            justify="left",
            font=("Segoe UI", 15),
            text_color=TEXT_CLR
        ).pack(padx=40, pady=10)

# =========================================================
# PATIENT PAGE
# =========================================================
class PatientPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")

        card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=25,
                            width=650, height=440)
        card.place(relx=0.55, rely=0.45, anchor="center")

        ctk.CTkLabel(card, text="Patient Details",
                     font=("Segoe UI", 22, "bold"),
                     text_color=SAFE_COLOR).pack(pady=15)

        self.entries = {}
        for field in ["Name", "Age", "Gender", "Phone", "Address"]:
            e = ctk.CTkEntry(card, placeholder_text=field, width=450)
            e.pack(pady=6)
            self.entries[field] = e

        ctk.CTkButton(
            card, text="Save Patient",
            fg_color=SAFE_COLOR, text_color="black",
            width=220, command=self.save_patient
        ).pack(pady=20)

    def save_patient(self):
        d = {k: v.get() for k, v in self.entries.items()}
        if not all(d.values()):
            messagebox.showerror("Error", "Fill all fields")
            return
        cur.execute(
            "INSERT INTO patients(name, age, gender, phone, address) VALUES (?,?,?,?,?)",
            (d["Name"], d["Age"], d["Gender"], d["Phone"], d["Address"])
        )
        conn.commit()
        messagebox.showinfo("Saved", "Patient data stored")

# =========================================================
# SCAN PAGE
# =========================================================
class ScanPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")

        card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=25,
                            width=650, height=360)
        card.place(relx=0.55, rely=0.45, anchor="center")

        ctk.CTkLabel(card, text="Retinal Image Upload",
                     font=("Segoe UI", 22, "bold"),
                     text_color=SAFE_COLOR).pack(pady=15)

        self.preview = ctk.CTkLabel(card, text="No image selected")
        self.preview.pack(pady=10)

        ctk.CTkButton(
            card, text="Upload Image",
            fg_color=SAFE_COLOR, text_color="black",
            command=self.upload
        ).pack(pady=10)

    def upload(self):
        f = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png")])
        if not f:
            return
        img = Image.open(f)
        img.thumbnail((320, 220))
        self.tkimg = CTkImage(light_image=img, dark_image=img, size=(320, 220))
        self.preview.configure(image=self.tkimg, text="")

# =========================================================
# REPORT PAGE (AI SEVERITY + COLOUR CHANGE)
# =========================================================
class ReportPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")

        self.card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=25,
                                 width=650, height=420)
        self.card.place(relx=0.55, rely=0.45, anchor="center")

        ctk.CTkLabel(self.card, text="AI Severity Prediction",
                     font=("Segoe UI", 22, "bold"),
                     text_color=SAFE_COLOR).pack(pady=15)

        self.severity_lbl = ctk.CTkLabel(
            self.card, text="Severity: --",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_CLR
        )
        self.severity_lbl.pack(pady=10)

        self.conf_bar = ctk.CTkProgressBar(
            self.card, width=450, progress_color=SAFE_COLOR
        )
        self.conf_bar.set(0)
        self.conf_bar.pack(pady=10)

        self.conf_txt = ctk.CTkLabel(
            self.card, text="Confidence: -- %",
            font=("Segoe UI", 14), text_color=TEXT_CLR
        )
        self.conf_txt.pack(pady=5)

        ctk.CTkButton(
            self.card, text="Run AI Model",
            fg_color=SAFE_COLOR, text_color="black",
            width=220, command=self.run_model
        ).pack(pady=20)

    def run_model(self):
        # ---- SIMULATED MODEL OUTPUT ----
        severity = random.choice(["No DR", "Mild", "Moderate", "Severe"])
        confidence = random.randint(60, 95)

        color = severity_color(severity)

        self.severity_lbl.configure(
            text=f"Severity: {severity}",
            text_color=color
        )
        self.conf_bar.configure(progress_color=color)
        self.conf_bar.set(confidence / 100)
        self.conf_txt.configure(
            text=f"Confidence: {confidence} %",
            text_color=color
        )

        cur.execute(
            "INSERT INTO reports(patient_id, severity, confidence, recommendation, referred, created_at)"
            " VALUES (1, ?, ?, ?, ?, ?)",
            (
                severity,
                confidence,
                recommendation_text(severity),
                "Yes" if color == DANGER_COLOR else "No",
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            )
        )
        conn.commit()
        messagebox.showinfo("Diagnosis Complete", "Medical report generated.")
        self.master.master.show(ReportDetailPage)

class ReportDetailPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")

        self.card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=16,
                                 width=720, height=460)
        self.card.place(relx=0.55, rely=0.5, anchor="center")

        ctk.CTkLabel(self.card, text="Medical Report",
                     font=("Segoe UI", 24, "bold"),
                     text_color=SAFE_COLOR).pack(pady=12)

        self.details = ctk.CTkLabel(self.card, text="",
                                    font=("Segoe UI", 14),
                                    text_color=TEXT_CLR,
                                    justify="left")
        self.details.pack(padx=24, pady=10, anchor="w")

        ctk.CTkButton(
            self.card, text="Refresh",
            fg_color=SAFE_COLOR, text_color="white",
            width=160, command=self.load_latest
        ).pack(pady=10)

        self.load_latest()

    def load_latest(self):
        cur.execute("SELECT severity, confidence, recommendation, referred, created_at FROM reports ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        if not row:
            self.details.configure(text="No report available yet.")
            return
        severity, confidence, recommendation, referred, created_at = row
        color = severity_color(severity)
        self.details.configure(
            text=(
                f"Date: {created_at}\n"
                f"Severity: {severity}\n"
                f"Confidence: {confidence} %\n"
                f"Recommendation: {recommendation}\n"
                f"Referral Required: {referred}"
            )
        )

# =========================================================
# ANALYTICS PAGE
# =========================================================
class AnalyticsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")

        ctk.CTkButton(
            self, text="View Severity Analytics",
            fg_color=SAFE_COLOR, text_color="black",
            width=260, command=self.graph
        ).place(relx=0.55, rely=0.45, anchor="center")

    def graph(self):
        cur.execute("SELECT severity, confidence FROM reports")
        rows = cur.fetchall()
        if not rows:
            messagebox.showinfo("No Data", "No reports available")
            return

        confidences = [r[1] for r in rows]
        colors = [severity_color(r[0]) for r in rows]

        plt.bar(range(len(confidences)), confidences, color=colors)
        plt.ylabel("Confidence %")
        plt.title("AI Severity Analysis")
        plt.show()

# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    RetinalAIApp().mainloop()
