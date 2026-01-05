import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog, messagebox
from PIL import Image
import sqlite3
import datetime
import os
import random
import matplotlib.pyplot as plt

# =========================================================
# SAFETY & THEME
# =========================================================
ctk.deactivate_automatic_dpi_awareness()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =========================================================
# DUAL COLOUR SYSTEM (ONLY TWO COLOURS)
# =========================================================
SAFE_COLOR = "#00E5FF"     # Blue–Cyan (No DR / Mild)
DANGER_COLOR = "#FF4D4D"   # Red (Moderate / Severe)
CARD_BG = "#0B2C3D"
TEXT_CLR = "#EAF6FF"
TOPBAR_BG = "#021826"
SIDEBAR_BG = "#021826"

# =========================================================
# DATABASE
# =========================================================
conn = sqlite3.connect("retinal_ai.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

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
            AboutPage,
            PatientPage,
            ScanPage,
            ReportPage,
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

        card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=25,
                            width=420, height=300)
        card.place(relx=0.5, rely=0.4, anchor="center")

        ctk.CTkLabel(card, text="System Login",
                     font=("Segoe UI", 22, "bold"),
                     text_color=SAFE_COLOR).pack(pady=25)

        self.user = ctk.CTkEntry(card, placeholder_text="Username", width=280)
        self.pwd = ctk.CTkEntry(card, placeholder_text="Password", show="*", width=280)
        self.user.pack(pady=10)
        self.pwd.pack(pady=10)

        ctk.CTkButton(
            card, text="Login",
            fg_color=SAFE_COLOR, text_color="black",
            width=200, command=self.login
        ).pack(pady=20)

    def login(self):
        u, p = self.user.get(), self.pwd.get()
        if not u or not p:
            messagebox.showerror("Error", "Enter credentials")
            return
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        if not cur.fetchone():
            cur.execute("INSERT INTO users VALUES (?,?)", (u, p))
            conn.commit()
        self.master.master.show(AboutPage)

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
