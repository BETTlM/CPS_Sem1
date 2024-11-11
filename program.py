import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, StringVar
import os
import pygame
import time
import threading
from modules import converter

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper Docs")
        self.root.geometry("1600x900")
        self.root.configure(bg="#1A1A1A")

        self.main_frame = tk.Frame(self.root, bg="#1A1A1A")
        self.main_frame.pack(expand=True, fill="both")

        self.create_login_frame()

        pygame.mixer.init()
        self.is_playing = False

    def create_login_frame(self):
        self.login_frame = tk.Frame(self.main_frame, bg="#2B2B2B", padx=20, pady=20, borderwidth=0)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(self.login_frame, text="Login", font=("Helvetica Neue", 32, "bold"), fg="#FFFFFF", bg="#2B2B2B")
        title_label.pack(pady=(0, 20))

        self.username_label = tk.Label(self.login_frame, text="Username:", font=("Helvetica Neue", 14), fg="#A3C1DA", bg="#2B2B2B")
        self.username_label.pack(anchor="w")
        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica Neue", 14), bg="#3B3B3B", fg="#FFFFFF", insertbackground="#FFFFFF", bd=0)
        self.username_entry.pack(fill="x", pady=(0, 10))

        self.password_label = tk.Label(self.login_frame, text="Password:", font=("Helvetica Neue", 14), fg="#A3C1DA", bg="#2B2B2B")
        self.password_label.pack(anchor="w")
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica Neue", 14), bg="#3B3B3B", fg="#FFFFFF", insertbackground="#FFFFFF", bd=0)
        self.password_entry.pack(fill="x", pady=(0, 20))

        login_button = tk.Button(self.login_frame, text="Login", font=("Helvetica Neue", 14), bg="#007AFF", fg="#FFFFFF", command=self.login, activebackground="#005BB5", bd=0, relief="flat")
        login_button.pack(fill="x")

        self.greet_label = tk.Label(self.main_frame, text="", font=("Helvetica Neue", 16, "bold"), fg="#A3C1DA", bg="#1A1A1A")
        self.greet_label.pack(pady=10)

        self.create_action_buttons()

    def create_action_buttons(self):
        button_style = {
            "font": ("Helvetica Neue", 14),
            "bg": "#007AFF",
            "fg": "#FFFFFF",
            "activebackground": "#005BB5",
            "bd": 0,
            "relief": "flat",
            "width": 20
        }

        self.upload_button = tk.Button(self.main_frame, text="Upload PDF", command=self.upload_pdf, **button_style)
        self.upload_button.pack(pady=10)
        self.upload_button.pack_forget()

        self.convert_button = tk.Button(self.main_frame, text="Convert PDF to Audio", command=self.convert_to_audio, **button_style)
        self.convert_button.pack(pady=10)
        self.convert_button.pack_forget()

        self.play_button = tk.Button(self.main_frame, text="Play Audio", command=self.play_audio, **button_style)
        self.play_button.pack(pady=10)
        self.play_button.pack_forget()

        self.progress_var = StringVar()
        self.progress_label = tk.Label(self.main_frame, textvariable=self.progress_var, bg="#1A1A1A", fg="#A3C1DA", font=("Helvetica Neue", 14))
        self.progress_label.pack(pady=10)
        self.progress_label.pack_forget()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "bettim" and password == "1":
            self.greet_label.config(text=f"Welcome, {username}!", fg="#A3C1DA")
            self.hide_login_fields()
            self.center_action_buttons()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def hide_login_fields(self):
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.password_label.pack_forget()
        self.password_entry.pack_forget()
        self.login_frame.pack_forget()

    def center_action_buttons(self):
        action_frame = tk.Frame(self.main_frame, bg="#1A1A1A")
        action_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.upload_button = tk.Button(action_frame, text="Upload PDF", command=self.upload_pdf, font=("Helvetica Neue", 14), bg="#007AFF", fg="#FFFFFF", activebackground="#005BB5", bd=0, relief="flat", width=20)
        self.upload_button.pack(pady=10)

        self.convert_button = tk.Button(action_frame, text="Convert PDF to Audio", command=self.convert_to_audio, font=("Helvetica Neue", 14), bg="#007AFF", fg="#FFFFFF", activebackground="#005BB5", bd=0, relief="flat", width=20)
        self.convert_button.pack(pady=10)

        self.play_button = tk.Button(action_frame, text="Play Audio", command=self.play_audio, font=("Helvetica Neue", 14), bg="#007AFF", fg="#FFFFFF", activebackground="#005BB5", bd=0, relief="flat", width=20)
        self.play_button.pack(pady=10)

        self.progress_label.pack_forget()

    def upload_pdf(self):
        pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if pdf_file:
            self.pdf_file = pdf_file
            global loc
            loc = pdf_file
            messagebox.showinfo("File Uploaded", f"PDF file '{os.path.basename(pdf_file)}' uploaded successfully.")

    def convert_to_audio(self):
        self.loading_screen = Toplevel(self.root)
        self.loading_screen.title("Loading...")
        self.loading_screen.geometry("300x150")
        self.loading_screen.configure(bg="#2B2B2B")
        self.loading_screen.overrideredirect(True)

        loading_label = tk.Label(self.loading_screen, text="Converting PDF to Audio...", font=("Helvetica Neue", 14), fg="#A3C1DA", bg="#2B2B2B")
        loading_label.pack(pady=20)

        threading.Thread(target=self.perform_conversion).start()

    def perform_conversion(self):
        try:
            converter.convert(pdflocation=loc)
            time.sleep(1)
            self.loading_screen.destroy()
            messagebox.showinfo("AUDIO CONVERTED", "Audio can be played now.")
        except Exception as error:
            self.loading_screen.destroy()
            messagebox.showerror("Conversion Error", f"An error occurred: {error}")

    def play_audio(self):
        audio_file = "recordedaudio.mp3"
        if os.path.exists(audio_file):
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

        else:
            messagebox.showerror("File Not Found", "Please convert a PDF to audio first.") 

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverterApp(root)
    root.mainloop()
